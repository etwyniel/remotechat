import socket
from threading import Thread
from time import sleep


class Server(socket.socket):

    def __init__(self):
        super().__init__()
        self.connections = []
        self.threads = []

    def accepting(self):
        while True:
            c, addr = self.accept()
            self.connections.append(c)
            t = Thread(target=self.responding, args=[c])
            self.threads.append(t)
            self.threads[-1].start()
            c.send(b'Connected\n')

    def responding(self, c):
        while True:
            messages = b''
            try:
                msg = c.recv(1024)
                if len(msg) > 0:
                    messages += msg
                    for x in self.connections:
                        x.send(messages)
            except ConnectionResetError:
                break
            



s = Server()
s.bind(('localhost', 102))
s.listen(5)

acc = Thread(target=s.accepting, daemon=True)
acc.start()

##rsp = Thread(target=s.responding, daemon=True)
##rsp.start()
##
input()
