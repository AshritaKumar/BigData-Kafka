from socket import *
import json
from client import Client
import sys

def handleForceExit(ClassName):
    object = ClassName()
    try:
        object.execute()
    except KeyboardInterrupt:
        object.closeConnection()
        sys.exit(1)


class Consumer(Client):

    def __init__(self):
        super(Consumer, self).__init__()

    def getTopic(self):
        self.topic = input('Input topic to subscribe or exit : ')

    def pack(self):
        message = json.dumps({'type':'subscribe','topic':self.topic})
        return message.encode('utf-8')

#receives data from the broker
    def receiveData(self):
        reply = self.socket.recv(self.size * 2)
        print(reply.decode('utf-8'))

    def subscribe(self):
        self.socket.send(self.pack())
        self.receiveData()

    def execute(self):
        self.run(self.subscribe)

if __name__ == "__main__":
    handleForceExit(Consumer)