import re
import time
import sys

import ioHandler
import messageParser

admins = set(["joshz"])
prefix = "&"
nick = "noFifthGlyph"

userName = "joshzNoFifthBot"
hostName = "joshz"
serverName = "irc.foonetic.net"
realName = "joshz"

con = ioHandler.IRCConnection("irc.foonetic.net")

con.setNick(nick)
con.setUser(userName, hostName, serverName, realName)

setMode = False # have we set +B yet?

unbans = {} # keep track of who we need to unban, and when.
while True: #main REPL
    input = con.receive()
    # Unban if needed
    cpy = unbans.copy()
    for u in cpy:
        if cpy[u][1] <= time.time():
            con.sendMessage("MODE " + cpy[u][0] + " -b " + u)
            del unbans[u]
    
    if input != "":
        print input

        mNick = messageParser.getNick(input)
        mChan = messageParser.getChannel(input)
        message = messageParser.getMessage(input)
        
        if "End of /MOTD command." in input and not(setMode):
            setMode = True
            # print "Setting mode +B"
            con.sendMessage("MODE " + nick + " +B") # indicate that we're a bot
            con.sendMessage("PRIVMSG NickServ IDENTIFY short-ead-aup-y") 
            if len(sys.argv) > 1:
                con.sendMessage("JOIN #" + sys.argv[1])
        
        pingResponse = messageParser.pingHandler(input)
        if pingResponse != "":
            con.sendMessage("PONG " + pingResponse)
            #print(repr(pingResponse))
            
        #print(repr(getMessage(input)))
        

        if ('e' in message or 'E' in message) and messageParser.getMessageType(input) == "PRIVMSG" and mNick != nick:
            print "Kicking " + mNick + " for " + message 
            con.sendMessage("KICK " + mChan + " " + mNick)
            con.sendMessage("MODE " + mChan + " +b " + mNick)
            unbans[mNick] = (mChan, time.time() + 15)


        if mNick in admins:  #admin-only commands
            if messageParser.hasPrefix(input):  #to avoid accidental commands, ensure command is prefaced with the prefix
                if messageParser.isQuit(input):
                    quitMessage = messageParser.partOrQuitMessage(input)
                    
                    if quitMessage != "":
                        con.sendMessage("QUIT" + " :" + quitMessage)
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
                    #print(repr(toPart))
                    
        
                    if toPart != "":
                        con.sendMessage("PART " + toPart + partMessage)
                        #print(repr(toPart + partMessage))
                
            if messageParser.getMessageType(input) == "INVITE": #auto-join on any invite (by an admin)
                con.sendMessage("JOIN " + message)

time.sleep(0.5)		
con.close()
