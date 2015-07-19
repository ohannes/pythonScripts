import os
import sys
import time

DEBUG_MODE = False

READ_MODE = "r"
WRITE_MODE = "w"
APPEND_MODE = "a"
BINARY_MODE = "b"
SYNC_BYTE = 0x47
TS_PACKET_LEN = 188
MIN_SYNC_CONDITION = 5
NON_FILTERED_PID = 0x2000
EMPTY_STR = ""
EXTENSION_SPLITTER = "."
SPACE = " "
NEW_LINE = "\n"
ARG_SPLITTER = "="
TS_EXTENSION = "ts"
DEFAULT_OUTPUT_FILE_NAME = "output"
OUTPUT_FOLDER_NAME_BASE = "TSanalyze"
PID_STR = "pid"
HEX  = "hex"
END = "END"

pids  = []
pids_cnt = []

INPUT_FILE_NAME = ""
OUTPUT_FILE_NAME = DEFAULT_OUTPUT_FILE_NAME + str(int(time.time() * 1000 * 1000))
PID_FILTER_ON = False
PID = NON_FILTERED_PID

def handleArgs():
	global DEBUG_MODE
	global INPUT_FILE_NAME
	global OUTPUT_FILE_NAME
	global PID_FILTER_ON
	global PID

	for arg in sys.argv[1:]:
		split = arg.split(ARG_SPLITTER)
		name = split[0]

		if len(split) == 1:
			if name.upper() == "DEBUG" or name.upper() == "D":
				DEBUG_MODE = True
			else:
				if DEBUG_MODE:
					print "ERROR: invalid argument!"
			continue
		value = split[1]

		if name.upper() == "INPUT_FILE" or name.upper() == "INPUT" or name.upper() == "IF" or name.upper() == "I":
			if os.path.exists(value):
				INPUT_FILE_NAME = value
			else:
				sys.exit("ERROR: " + value + " does not exist!")

		elif name.upper() == "OUTPUT_FILE" or name.upper() == "OUTPUT" or name.upper() == "OF" or name.upper() == "O":
			if value == EMPTY_STR:
				if DEBUG_MODE:
					print "ERROR: invalid output file name:", value
					print "default output file name will be used:", OUTPUT_FILE_NAME
			else:
				OUTPUT_FILE_NAME = value

		elif name.upper() == "PID_FILTER" or name.upper() == "PID" or name.upper() == "PF" or name.upper() == "P":
			try:
				PID = int(value)
				if PID >= 0 and PID <= NON_FILTERED_PID:
					PID_FILTER_ON = True
				else:
					if DEBUG_MODE:
						print "ERROR: invalid pid"
					PID_FILTER_ON = False
			except:
				if DEBUG_MODE:
					print "ERROR: invalid pid"
				PID_FILTER_ON = False

		else:
			if DEBUG_MODE:
				print "ERROR: invalid argument!"

def getContent(fileName):
	global FILE_EXTENSION
	if not os.path.exists(fileName):
		sys.exit("ERROR: input file " + fileName + " does not exists!")
	FILE_EXTENSION = fileName.split(".")[-1]
	ftr = open(fileName, READ_MODE + BINARY_MODE)
	content = ftr.read()
	ftr.close()
	return content

def hasSync(content):
	index = 0
	while ord(content[index]) != SYNC_BYTE:
		index += 1
		if index == len(content) - 1:
			print "index:", index
			return -1
	content = content[index:]
	for i in range(MIN_SYNC_CONDITION):
		byte = ord(content[i*TS_PACKET_LEN])
		if byte != SYNC_BYTE:
			return -1
	return index

def getPid(packet):
	return (ord(packet[1]) & 0x1F) * 0x100 + ord(packet[2])

def writePacket(packetFileName, packet):
	ftw = open(packetFileName, APPEND_MODE)
	for byte in packet:
		ftw.write(str(hex(ord(byte)))[2:] + SPACE)
	ftw.write(NEW_LINE)
	ftw.close()

def writeStream(streamFileName, packet):
	ftw = open(streamFileName, APPEND_MODE + BINARY_MODE)
	for byte in packet:
		ftw.write(byte)
	ftw.close()

def writeAllStream(content):
	ftw = open(OUTPUT_FILE_NAME, WRITE_MODE+BINARY_MODE)
	for byte in content:
		ftw.write(byte)
	ftw.close()

def filterPid(pid, packet):
	global pid_cnt
	if PID != NON_FILTERED_PID and pid != PID:
		return
	for byte in packet:
		outputFile.write(byte)
		outputFile2.write(str(hex(ord(byte))) + SPACE)
	outputFile2.write(NEW_LINE)
	pid_cnt += 1

def removeFile(*files):
	for fileName in files:
		if os.path.exists(fileName):
			os.remove(fileName)

handleArgs()

OUTPUT_FOLDER_NAME = OUTPUT_FOLDER_NAME_BASE + "_of_" + INPUT_FILE_NAME

content = getContent(INPUT_FILE_NAME)

if DEBUG_MODE:
	print len(content), "bytes has been read."

sync_index = hasSync(content)

if(sync_index != -1):
	if DEBUG_MODE:
		print "The stream has sync."
	print sync_index
	content = content[sync_index:]
else:
	sys.exit("The stream does not have sync.")

if len(content) % TS_PACKET_LEN != 0:
	content = content[:-(len(content) % TS_PACKET_LEN)]
	#sys.exit("The content length is not a multiple of 188 (TS PACKET LENGTH)")

numOfPackets = len(content) / TS_PACKET_LEN

if DEBUG_MODE:
	print "The content length is a multiple of 188 (TS PACKET LENGTH)."
	print "There are", numOfPackets, "packets in the stream."

if PID_FILTER_ON:
	removeFile(OUTPUT_FILE_NAME)
	outputFile = open(OUTPUT_FILE_NAME, WRITE_MODE+BINARY_MODE)
	outputFile2 = open(OUTPUT_FILE_NAME + EXTENSION_SPLITTER + HEX, WRITE_MODE)
	pid_cnt = 0
	if DEBUG_MODE:
		print "applying pid filter (" + str(PID) + ")..."
else:
	if not os.path.exists(OUTPUT_FOLDER_NAME):
		os.mkdir(OUTPUT_FOLDER_NAME)
	os.chdir(OUTPUT_FOLDER_NAME)
	if DEBUG_MODE:
		print "splitting the stream by pids..."

for i in range(numOfPackets):
	packet = content[i*TS_PACKET_LEN:(i+1)*TS_PACKET_LEN]
	pid = getPid(packet)
	if PID_FILTER_ON:
		filterPid(pid, packet)
		continue
	packetFileName = PID_STR + str(pid) + EXTENSION_SPLITTER + HEX
	streamFileName = PID_STR + str(pid) + EXTENSION_SPLITTER + FILE_EXTENSION
	if not pid in pids:
		pids.append(pid)
		pids_cnt.append(0)
		removeFile(streamFileName, packetFileName)
	writePacket(packetFileName, packet)
	writeStream(streamFileName, packet)
	pids_cnt[pids.index(pid)] += 1

if PID_FILTER_ON:
	outputFile.close()
	outputFile2.close()
	if DEBUG_MODE:
		print pid_cnt, "packets with pid", PID

if DEBUG_MODE:
	for i in range(len(pids)):
		print pids_cnt[i], "packets with pid", pids[i]


