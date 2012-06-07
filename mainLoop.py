import time
import sys

import config
import ircConnection
import messageParser


def repl(chans):

    con = ircConnection.IRCConnection(config.server)

    con.setNick(config.nick)
    con.setUser(config.userName,
                config.hostName,
                config.server,
                config.realName)

    setBot = False  # have we identified as a bot yet?

    devoiced = {}  # keep track of who's devoiced and when they can be revoiced
    while True:  # main REPL
        fromServer = con.receive()

        #  +v users whose punishments have expired
        cpy = devoiced.copy()
        for user in cpy: # cpy[u] is a tuple with (chan, time)
            if cpy[user][1] <= time.time():
                con.sendMessage("MODE " + cpy[user][0] + " +v " + user)
                del devoiced[user]

        if fromServer != "":
            pingResponse = messageParser.pingHandler(fromServer)
            if pingResponse != "":
                con.sendMessage("PONG " + pingResponse)
                continue

            print fromServer

            mNick = messageParser.getNick(fromServer)
            mChan = messageParser.getChannel(fromServer)
            message = messageParser.getMessage(fromServer)

            if "End of /MOTD command." in fromServer and not setBot:
                setBot = True

                con.setBot(config.nick)
                if config.password != "":
                    con.authenticate(config.password)

                for chan in chans:
                    con.join(chan)


            if (('e' in message or 'E' in message) and
                    messageParser.getMessageType(fromServer) == "PRIVMSG" and
                    mNick != config.nick): # don't devoice ourselves

                badWord = ""
                for word in message.split():
                    if 'e' in word or 'E' in word:
                        badWord = word
                        break
                con.sendMessage("PRIVMSG " + mChan +
                                        " '%s' is a horrid word!" % badWord)
                con.sendMessage("MODE " + mChan + " -v " + mNick)
                devoiced[mNick] = (mChan, time.time() + 15)
           
            # make sure that new people get to talk,
            # and that rejoining doesn't get around a -v
            if (messageParser.getMessageType(fromServer) == "JOIN" and
                    mNick not in devoiced): 
                con.sendMessage("MODE " + messageParser.chanFromJoin(fromServer)
                                          + " +v " + mNick)

            if mNick in config.admins:  #admin-only commands
                #to avoid accidental commands, ensure command has our prefix
                if messageParser.hasPrefix(fromServer):

                    if messageParser.isQuit(fromServer):
                        quitMessage = messageParser.partOrQuitMessage(fromServer)

                        con.quit(quitMessage)
                        break

                    if messageParser.isPart(fromServer):
                        partMessage = messageParser.partOrQuitMessage(fromServer)

                        if messageParser.partDefault(fromServer):
                            toPart = mChan # part current chan if none specified
                        else:
                            toPart = messageParser.getPartChannel(fromServer)

                        con.part(partMessage, toPart)

                #auto-join on any invite (by an admin)
                if messageParser.getMessageType(fromServer) == "INVITE":
                    con.join(message)

    time.sleep(0.5)
    con.close()

def main():
    repl(sys.argv[1:])

if __name__ == '__main__':
    main()
