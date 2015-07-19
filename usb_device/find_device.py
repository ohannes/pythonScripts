import os

devices = "/sys/bus/usb/devices/"
ID = "0x024f"
idProductStr = "idProduct"

def find_device(dirList, idProduct):
	print dirList
	for fileName in dirList:
		print os.getcwd()
		if os.path.isdir(fileName):
			fileList = os.listdir(fileName)
			os.chdir(fileName)
			print os.getcwd()
			for nameFile in fileList:
				if nameFile == idProductStr:
					try:
						ftr = open(nameFile, "r")
						PRODUCT_ID = ftr.read()
						ftr.close()
						print PRODUCT_ID
						if PRODUCT_ID == idProduct:
							print os.getcwd(), PRODUCT_ID
							exit(1)
					except:
						print "ERROR file could be opened"
			os.chdir('..')
fileList = os.listdir(devices)
os.chdir(devices)
find_device(fileList, ID)
print ID + " could not be found"
