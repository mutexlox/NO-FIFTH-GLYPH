import re

import config

prefix = config.prefix

# Useful test strings:
# Normal: :Emi!~chatzilla@hide-F95A65D1.hsd1.md.comcast.net PRIVMSG Emijoshzbot :&quit test
# IPv6: :TGB!~user@1A1ED16D:89725881:A8F36EFF:IP PRIVMSG #xkcd-abcdfghijklmnopqrstuvwxyz :ok.
# Join: :joshztests!43bc0182@hide-6C77D8AA.mibbit.com JOIN :##joshzTestsHisBot 

# Returns the nick string from an IRC message
#   (nicks never contain ! and always have ! following them
nick = re.compile(r":([^!]+)")

# Get the user-sent message from an IRC PRIVMSG
message = re.compile(r":[^:]+\ :(.*$)")

# Get the type of message from an IRC message
#   (e.g. PRIVMSG, KICK, etc)
messageType = re.compile(" ([A-Z]*)")

# Get the channel a message was sent to from an IRC message
channel = re.compile("\S+ \S+ (\S+)")  # \S is any non-whitespace char

# Determines whether the sent message is a PING
# PING :irc.foonet.bar
ping = re.compile("^PING :(.*?)\r")

# In a JOIN message, determines the chan being joined to.
join = re.compile("JOIN :([^ ]+?)\r\n")

# Determines whether or not something is a user-given part command
part = re.compile("^" + prefix + "part")

# Determines whether a part command has channel arguments
partNoArgs = re.compile(prefix + "part(\r| [^&#+!].*)")

# If given a part or quit command, get the message the user specified for the
#   bot to part or quit with (e.g., &part #foo Message text.)
partQuitMessage = re.compile(prefix + "(?:quit|part)(?: [#&+!]\w+)* (.*?)\r")

# Given a user message, determine whether it's a command to the bot to quit
quit = re.compile("^" + prefix + "quit")

# Get the channel from which to part, given a part command from a user
channelToPart = re.compile("part ([&#+!][^, :]+)")

def getGroup(match, group=1):
    '''Given a match for a regex, returns the
       specified group or "" if there is no match.
    '''
    return "" if match is None else match.group(group)

def getMessage(ircMessage):
    '''Given an IRC message, returns the message being sent by the user.
    '''
    return getGroup(re.search(message, ircMessage))

def hasPrefix(ircMessage):
    '''Returns true iff the user-sent message has the command prefix.
    '''
    message = getMessage(ircMessage)
    return message.startswith(prefix)

def getNick(ircMessage):
    '''Given an IRC message, returns the nick string (only if it's valid).
    '''
    return getGroup(re.search(nick, ircMessage))

def getMessageType(ircMessage):
    '''Given an IRC message, return type of message (PRIVMSG, INVITE, etc)
    '''
    return getGroup(re.search(messageType, ircMessage))

def getChannel(ircMessage):
    '''Given an IRC message, return the channel in which it was sent.
    '''
    return getGroup(re.search(channel, ircMessage))

def pingHandler(ircMessage):
    '''Given an IRC message, return the server to PONG if it's a PING,
       else the empty string.
    '''
    return getGroup(re.search(ping, ircMessage))

def chanFromJoin(ircMessage):
    '''Given an IRC message, return the chan that was joined if it's a JOIN,
       else the empty string.
    '''
    return getGroup(re.search(join, ircMessage))

def isPart(ircMessage):
    '''Returns true if and only if the given message is a part command
    '''
    partMatch = re.search(part, getMessage(ircMessage))

    return partMatch is not None

def partDefault(ircMessage):
    '''Returns true iff the message is a part command without
        channel arguments
    '''
    partNoArgsMatch = re.search(partNoArgs, getMessage(ircMessage))

    return partNoArgsMatch is not None

def partOrQuitMessage(ircMessage):
    '''Given a message which is a part or quit command,
        find the message to be sent with the quit
        (e.g. QUIT Message text -> Message text)
     '''
    return getGroup(re.search(partQuitMessage, ircMessage))

def isQuit(ircMessage):
    '''Returns true if and only if the message is a quit command from user
    '''
    quitMatch = re.search(quit, getMessage(ircMessage))
    return quitMatch is not None

def getPartChannel(ircMessage):
    '''Given a part command, find the channel from which we want to part.
    '''
    return getGroup(re.search(channelToPart, ircMessage))

def isPM(ircMessage):
    '''Return true iff the given command is a private message to just us.
    '''
    return getChannel(ircMessage) == config.nick
