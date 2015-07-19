import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

tempFile = "temp"
wlan2 = "wlan2"

def getIPaddr():
	os.system("ifconfig > " + tempFile)
	lines = getFileLines(tempFile)
	os.remove(tempFile)
	for i in range(len(lines)):
		if wlan2 in lines[i]:
			j = 0
			while lines[i+1][j] != ":":
				j += 1
			j += 1
			ipAddr = ""
			while lines[i+1][j] != " ":
				ipAddr += lines[i+1][j]
				j += 1
			return ipAddr

print getIPaddr()
