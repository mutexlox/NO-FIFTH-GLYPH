#!/usr/bin/env python

import re
import time

import ioHandler
import messageParser
# import utilFunctions

admins = set(["joshz"])
prefix = "&"
nick = "noFifthGlyph"

userName = "joshzNoFifthBot"
hostName = "joshz"
serverName = "irc.foonetic.net"
realName = "joshz"

con = ioHandler.ircConnection("irc.foonetic.net")

con.setNick(nick)
con.setUser(userName, hostName, serverName, realName)

setMode = False # have we set +B yet?

unbans = {} # keep track of who we need to unban, and when.
while True: #main REPL
    input = con.receive()
    print input

    mNick = messageParser.getNick(input)

    
    if "End of /MOTD command." in input and not(setMode):
        setMode = True
        print "Setting mode +B"
        con.sendMessage("MODE " + nick + " +B") # indicate that we're a bot
    
    pingResponse = messageParser.pingHandler(input)
    if pingResponse != "":
        con.sendMessage("PONG " + pingResponse)
        #print(repr(pingResponse))
		
    #print(repr(getMessage(input)))
    
    message = messageParser.getMessage(input)

    for u in unbans:
        if unbans[u] < time.time():
            con.sendMessage("MODE " + messageParser.getChannel(input) + " -b" + u)


    if ('e' in messageParser.getMessage(input) or 'E' in messageParser.getMessage(input)) and ('foonetic.net' not in input):
        # print "LOLOL " + messageParser.getNick(input)
        con.sendMessage("KICK " + messageParser.getChannel(input) + " " + mNick)
        con.sendMessage("MODE " + messageParser.getChannel(input) + " +b " + mNick)
        unbans[mNick] = (messageParser.getChannel(input), time.time() + 60)


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
                    toPart = messageParser.getChannel(input)
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
