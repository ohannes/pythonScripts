import sys, os, socket, threading, time
sys.path.append(os.environ["ohannes"])
from ohannes import *

BUFFER_SIZE = 1024
server = None

class SessionMessageSender(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.is_connected = True
    def send(self, message):
        if self.is_connected:
            self.conn.send(message)

class SessionMessageReceiver(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.is_connected = True
        self.start()
    def receive(self, size):
        if self.is_connected:
            return self.conn.recv(size)
        return ""
    def run(self):
        global server
        while True:
            if self.is_connected:
                message = self.receive(BUFFER_SIZE)
                if len(message) > 0:
                    print "\n", "###", self.addr, "->", message, "###", "\n"
                    for session in server.sessions:
                        session.sender.send(message)
                else:
                    self.is_connected = False
                    break
            else:
                break

class ServerSession(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.is_connected = True
        self.sender = SessionMessageSender(self.conn, self.addr)
        self.receiver = SessionMessageReceiver(self.conn, self.addr)

class TCPserver(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        self.sessions = []
        self.start()
    def accept(self):
    	print "Waiting for connection..."
    	conn, addr = self.socket.accept()
    	session = ServerSession(conn, addr)
        self.sessions.append(session)
    def run(self):
        while True:
            self.accept();

TCP_IP = '0.0.0.0'
TCP_PORT = getIntArg(1, 1)

server = TCPserver(TCP_IP, TCP_PORT)
while True:
    message = raw_input("Enter the message to sent: ")
    for session in server.sessions:
        session.sender.send(message)