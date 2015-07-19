import os, sys, threading, time
sys.path.append(os.environ["ohannes"])
from ohannes import *

class myThread(threading.Thread):
	def __init__(self, command):
		self.command = command
		threading.Thread.__init__(self)
	def run(self):
		os.system(self.command)


number_of_players = getIntArg(1, 1)
threads = []

for i in range(number_of_players):
	thread = myThread("vlc udp/ts://@localhost:400" + str(i))
	threads.append(thread)

for thread in threads:
	thread.start()

audio_thread = myThread("vlc udp/ts://@localhost:5000")
audio_thread.start()
