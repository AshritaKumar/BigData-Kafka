import os
from socket import socket, AF_INET, SOCK_DGRAM
import sys
from datetime import datetime

def parseInt(stringToParse):
    try:
        if not stringToParse: return None
        return int(stringToParse)
    except:
        print('Cannot convert string to integer')
        return None

class Template:

    # default server props
    PORT = 12000
    IP = 'localhost'

    # default buffer size
    BUFFER_SIZE = 1024

    def __init__(self):
        self.socket = socket(AF_INET,SOCK_DGRAM)
        self.serverIP= Template.IP
        self.serverPort = parseInt(os.environ.get('PORT', None)) or Template.PORT
        self.size = Template.BUFFER_SIZE

    def log(self, message):
        print(f'{datetime.now()}: {message}')

    def execute(self):
        raise NotImplementedError

    def closeConnection(self):
        self.socket.close()

    def shouldExit(self, topic):
        if topic == 'exit_':
            self.closeConnection()
            sys.exit(0)

class Client(Template):

    def __init__(self):
        super(Client, self).__init__()
        self.serverAddress = (self.serverIP,self.serverPort)
        self.topic = ""

    def run(self, callable):
        self.socket.connect(self.serverAddress)
        addr = self.socket.getsockname()
        self.log(f'Connected from {addr[0]}:{addr[1]}')
        while True:
            self.getTopic()
            self.shouldExit(self.topic)
            callable()