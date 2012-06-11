import socket
import select

import config

class IRCConnection:
    def __init__(self, serverName, port=6667):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((serverName, port))
        self.connection.setblocking(0)

    def sendMessage(self, toSend):
        '''Helper function that sends the given
           string as an IRC message.
        '''
        if not toSend.startswith("PONG"):
            print toSend
        self.connection.send(str(toSend) + "\r\n")

    def receive(self):
        '''Recieve 512 bytes from the connection (512 bytes == 1 message)
        '''
        # time out after a reasonable period of time so we revoice quickly
        ready = select.select([self.connection], [], [], 0.2)
        if ready[0]:
            return str(self.connection.recv(512))
        else:
            return None

    def setNick(self, nick):
        '''Sets the nick to given string.
        '''
        self.sendMessage("NICK " + nick)

    def setUser(self, userName, hostName, serverName, realName):
        '''Set the user info as given.
        '''
        self.sendMessage("USER " + userName + " " +
                                   hostName + " " +
                                   serverName + " :" +
                                   realName)

    def authenticate(self, password):
        '''Authenticate with NickServ with given password.
        '''
        self.sendMessage("PRIVMSG NickServ IDENTIFY " + password)

    def setBot(self, nick):
        '''Tell the server that we're a bot. (Note: This is network-dependent!)
        '''
        config.botIdentify(self, botNick=nick)

    def reply(self, toSend, nick, chan, isPM):
        sendTo = nick if isPM else chan
        self.sendMessage("PRIVMSG " + sendTo + " :" + toSend)

    def quit(self, quitMessage):
        if quitMessage == "":
            self.sendMessage("QUIT")
        else:
            self.sendMessage("QUIT :" + quitMessage)

    def part(self, partMessage, chan):
        if chan != "":
            if partMessage == "":
                self.sendMessage("PART " + chan)
            else:
                self.sendMessage("PART " + chan + " :" + partMessage)

    def join(self, chan):
        self.sendMessage("JOIN " + chan)

    def close(self):
        '''Close the connection.
        '''
        self.connection.close()
