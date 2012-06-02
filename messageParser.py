import re

import config

prefix = config.prefix

# Useful test strings:
# Normal: :Emi!~chatzilla@hide-F95A65D1.hsd1.md.comcast.net PRIVMSG Emijoshzbot :&quit test
# IPv6: :TGB!~user@1A1ED16D:89725881:A8F36EFF:IP PRIVMSG #xkcd-abcdfghijklmnopqrstuvwxyz :ok.
# Join: :joshztests!43bc0182@hide-6C77D8AA.mibbit.com JOIN :##joshzTestsHisBot 

# Returns the nick string from an IRC message,
#     validating against the valid nick characters and length.
# nick: letters, numbers, and the characters -_[]{}\|`^.
#     The nickname cannot begin with a digit or a hyphen.
nick = re.compile(r":([^\d\-][A-Za-z0-9\-_[\]{}\\|`^]{0,29})")

# Get the user-sent message from an IRC PRIVMSG
message = re.compile(r"[^:]+\ :(.*$)")

# Get the type of message from an IRC message
#   (e.g. PRIVMSG, KICK, etc)
messageType = re.compile(" ([A-Z]*)")

# Get the channel a message was sent to from an IRC message
channel = re.compile("\S+ \S+ (\S+)")

# Determines whether the sent message is a PING;
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
quitPattern = re.compile("^" + prefix + "quit")

# Get the channel from which to part, given a part command from a user
channelToPart = re.compile("part ([&#+!][^, :]+)")


def getMessage(ircMessage):
    '''Given an IRC message, returns the message being sent by the user.
    
    '''
    messageMatch = re.search(message, ircMessage)
    try:
        return messageMatch.group(1)
    except:
        return ""

def hasPrefix(ircMessage):
    '''Returns true iff the user-sent message has our command prefix.
    
    '''
    message = getMessage(ircMessage)
    return message.startswith(prefix)

def getNick(ircMessage):
    '''Given an IRC message, returns the nick string (only if it's valid).
    
    '''
    nickMatch = re.search(nick, ircMessage)
    try:
        return nickMatch.group(1)
    except:
        return ""
        
def getMessageType(ircMessage):
    '''Given a properly-formatted IRC message, return type of message
        (e.g. PRIVMSG, INVITE, etc)
        
    '''
    messageTypeMatch = re.search(messageType, ircMessage)
    try:
        return messageTypeMatch.group(1)
    except:
        return ""
        
def getChannel(ircMessage):
    '''Given an IRC message, return the channel in which it was sent.
    
    '''
    channelMatch = re.search(channel, ircMessage)
    try:
        return channelMatch.group(1)
    except:
        return ""

def pingHandler(ircMessage):
    '''Given an IRC message,
    return the server to PONG if it's a PING, else the empty string.
    
    '''
    pingMatch = re.search(ping, ircMessage)
    try:
        return pingMatch.group(1)
    except:
        return ""

def chanFromJoin(ircMessage):
    '''Given an IRC message, return the chan that was joined if it's a JOIN,
    else the empty string.

    '''
    joinMatch = re.search(join, ircMessage)
    try:
        return joinMatch.group(1)
    except:
        return ""

def isPart(ircMessage):
    '''Returns true if and only if the given message is a part command
    
    '''
    message = getMessage(ircMessage)
    res = re.search(part, message)
    if res == None:
        return False
    else:
        return True
    
def partDefault(ircMessage):
    '''Returns true iff the message is a part command without
        channel arguments
        
    '''
    message = getMessage(ircMessage)
    res = re.search(partNoArgs, message)
    if res == None:
        return False
    else:
        return True

def partOrQuitMessage(ircMessage):
    '''Given a message which is a part or quit command,
        find the message to be sent with the quit
        (e.g. QUIT Message text -> Message text)'''
    partQuitMessageMatch = re.search(partQuitMessage, ircMessage)
    try:
        return partQuitMessageMatch.group(1)
    except:
        return ""

def isQuit(ircMessage):
    '''Returns true if and only if the message is a quit command from user'''
    res = re.search(quitPattern, getMessage(ircMessage))
    if res == None:
        return False
    else:
        return True
    
def getPartChannel(ircMessage):
    '''Given a part command, find the channel from which we want to part.'''
    channelToPartMatch = re.search(channelToPart, ircMessage)
    try:
        return channelToPartMatch.group(1)
    except:
        return ""
