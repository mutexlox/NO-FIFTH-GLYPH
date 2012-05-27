import socket
import select

class IRCConnection:
    def __init__(self, serverName, port=6667):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((serverName, port))
        self.connection.setblocking(0)
	
    def sendMessage(self, toSend):
        '''Helper function that sends the given
           string as an IRC message, appending \r\n.
        
        '''
        self.connection.send(str(toSend + "\r\n")) 

    def receive(self):
        '''Recieve 512 bytes from the connection (512 bytes == 1 message)
        
        '''
        # make sure we time out after 0.02 seconds so we unban quickly
        ready = select.select([self.connection], [], [], 0.02)
        if ready[0]:
            return str(self.connection.recv(512)) 
        else:
            return ""
		
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

    def close(self):
        '''Close the connection.
        
        ''' 
        self.connection.close()
