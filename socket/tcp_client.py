import sys, os, socket, threading, time
from PyQt4.QtGui import *
sys.path.append(os.environ["ohannes"])
from ohannes import *

BUFFER_SIZE = 1024

class TCPsender(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):
        while True:
            if self.client.is_connected:
                message = raw_input("Enter the message to sent: ")
                if message.upper() == "EXIT":
                    break
                else:
                    self.client.send(message)
                    if not self.client.is_connected:
                        print "Connection Lost"
                        break
            else:
                print "Connection Lost"
                break

class TCPclient(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.is_connected = True
        self.start()
    def receive(self, size):
        if self.is_connected:
            return self.socket.recv(size)
        return ""
    def send(self, message):
        if self.is_connected:
            self.socket.send(message)
    def run(self):
        while True:
            if self.is_connected:
                message = self.receive(BUFFER_SIZE)
                if len(message) > 0:
                    #print "response(" + str(len(message)) + "):", message
                    print "\n### " + message + " ###\n"
                    #label = QLabel(message, None)
                    #label.show()
                else:
                    self.is_connected = False
                    break
            else:
                break

TCP_IP = "195.87.189.166"
TCP_PORT = 1018

if len(sys.argv) > 1:
    TCP_IP = getStrArg(1, 2)
    TCP_PORT = getIntArg(2, 2)
else:
    print "GIB TESTING MODE is active"

client = TCPclient(TCP_IP, TCP_PORT)
client.connect()
sender = TCPsender(client)
sender.start()

#app = QApplication(sys.argv)
#app.exec_()

while True:
    time.sleep(1)