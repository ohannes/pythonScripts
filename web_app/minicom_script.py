import os

NEW_APP = raw_input("application name: ")

def getLines(fileName):
	try:
		ftr = open(fileName, "r")
	except:
		print "ERROR: file could not be opened...", fileName
		exit(1)
	lines = ftr.readlines()
	ftr.close()
	return lines

def getIPaddr():
	tempFile = "temp"
	wlan2 = "wlan2"
	os.system("ifconfig > " + tempFile)
	lines = getLines(tempFile)
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

def mountAndLink():
	#os.system("minicom -con")
	print("minicom -con")
	#method to send commands to minicom needed
	print("ctrl-z")
	print("mkdir -p /dev/shm/nfs")
	print("mount -t nfs " + getIPaddr() + ":/home/arcelik/projects -o nolock,rsize=4096,wsize=4096 /dev/shm/nfs")
	print("mount -o remount,rw /applications")
	print("cd")
	print("cd Customer/appstore/install/6")
	print("mv app app_yedek")
	print("ln -sf /tmp/nfs/apps/source/widgets/src/widgets/" + NEW_APP + "/WebContent app")
	print("fg")

mountAndLink()
