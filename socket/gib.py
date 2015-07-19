import sys, os, socket, time
sys.path.append(os.environ["ohannes"])
from ohannes import *

BUFFER_SIZE = 2048
TCP_IP = '127.0.0.1'
TCP_PORT = 4001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
	print "Waiting for connection..."
	conn, addr = s.accept()
	print 'Connection address:', addr

	while 1:
		#time.sleep(100)
		msg = conn.recv(BUFFER_SIZE)
		if not msg: break
		length = len(msg)
		print "message length:", length
		resp = ""

		target0 = msg[3]
		target1 = msg[4]
		src0 = msg[5]
		src1 = msg[6]

		resp += msg[0]
		resp += msg[1]
		resp += msg[2]
		resp += src0
		resp += src1
		resp += target0
		resp += target1
		for i in range(length - 7):
			resp += msg[i+7]

		print "Sleeping"
		#time.sleep(100)
		print "Awaken"
		conn.send(resp)
		print "response length:", len(resp)
		if msg.upper() == "EXIT":
			conn.close()
			sys.exit("");
			break
		break;