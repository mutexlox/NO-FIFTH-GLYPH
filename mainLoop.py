import re
import time
import sys

import config
import ioHandler
import messageParser


def repl(server, password, chans):

    con = ioHandler.IRCConnection(server)

    con.setNick(config.nick)
    con.setUser(config.userName, config.hostName, server, config.realName)

    setMode = False # have we set +B yet?

    unbans = {} # keep track of who we need to unban, and when.
    while True: #main REPL
        input = con.receive()
        # Unban if needed
        cpy = unbans.copy()
        for user in cpy: # cpy[u] is a tuple with (chan, time)
            if cpy[user][1] <= time.time():
                con.sendMessage("MODE " + cpy[user][0] + " -b " + user)
                del unbans[user]

        if input != "":
            print input

            mNick = messageParser.getNick(input)
            mChan = messageParser.getChannel(input)
            message = messageParser.getMessage(input)

            if "End of /MOTD command." in input and not(setMode):
                setMode = True
                # print "Setting mode +B"
                con.sendMessage("MODE " + config.nick + " +B") # bot flag
                con.sendMessage("PRIVMSG NickServ IDENTIFY " + password) 
                for chan in chans:
                    con.sendMessage("JOIN " + chan)

            pingResponse = messageParser.pingHandler(input)
            if pingResponse != "":
                con.sendMessage("PONG " + pingResponse)


            if ('e' in message or 'E' in message) and \
                    messageParser.getMessageType(input) == "PRIVMSG" and \
                    mNick != config.nick: # don't kick ourselves

                badWord = ""
                for word in message.split():
                    if 'e' in word or 'E' in word:
                        badWord = word
                        break
                
                con.sendMessage("MODE " + mChan + " +b " + mNick)
                con.sendMessage("KICK " + mChan + " " + mNick + " :" + badWord)
                unbans[mNick] = (mChan, time.time() + 15)


            if mNick in config.admins:  #admin-only commands
                #to avoid accidental commands, ensure command has our prefix
                if messageParser.hasPrefix(input):  
                    if messageParser.isQuit(input):
                        quitMessage = messageParser.partOrQuitMessage(input)
                        
                        if quitMessage != "":
                            con.sendMessage("QUIT :" + quitMessage)
                        else:
                            con.sendMessage("QUIT")
                        break
                    if messageParser.isPart(input):
                        partMessage = messageParser.partOrQuitMessage(input)
                        #print(repr(partMessage))

                        if partMessage != "":
                            partMessage = " " + partMessage
                                
                        if messageParser.partDefault(input):
                            toPart = mChan # part current chan if none specified
                        else:
                            toPart = messageParser.getPartChannel(input)
           

                        if toPart != "":
                            con.sendMessage("PART " + toPart + partMessage)
                            #print(repr(toPart + partMessage))
                #auto-join on any invite (by an admin) 
                if messageParser.getMessageType(input) == "INVITE": 
                    con.sendMessage("JOIN " + message)

    time.sleep(0.5)		
    con.close()

def main():
    if len(sys.argv) < 3:
        print "Usage: python mainLoop.py server password [chans]"
    else:
        repl(sys.argv[1], sys.argv[2], sys.argv[3:])

if __name__ == '__main__':
    main()
