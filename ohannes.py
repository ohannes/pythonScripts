import os, sys
from types import *

ERROR = 0
WARNING = 1
STATUS = 2
INFO = 3
LOOP = 4

level_strings = ["ERROR", "WARNING", "STATUS", "INFO", "LOOP"]

#file modes
read_mode = "r"
write_mode = "w"
append_mode = "a"

#special characters
EMPTY_STR = ""
EOL = "\n"
TAB = "\t"
SPACE = " "
SHARP = "#"
CREATE_DIR_CMD = "mkdir"
COPY_CMD = "mv"
PATH_SPLITTER = "/"
DUPLICATE_NAME_SIGN = "_"
PARENT_DIR = ".."
EXTENSION_SPLITTER = "."
PARAMETER_SPLITTER = " "
LAST_INDEX = -1
INIT_STR = ""
START = "START"
END = "END"

#general
def printMessage(level, message, source):
	print level_strings[level] + ": " + message + " <-> " + source
	if level == 0:
		exit(1)

#Konsole arguments
def checkArgumentExists(index):
	return len(sys.argv) > index

def getStrArg(index, total_argument_number):
	if not checkArgumentExists(index):
		printMessage(ERROR, "not enough arguments: " + str(total_argument_number) + " arguments required", "getStrArg")
	return sys.argv[index]

def getIntArg(index, total_argument_number, base=10):
	if not checkArgumentExists(index):
		printMessage(ERROR, "not enough arguments: " + str(total_argument_number) + " arguments required", "getIntArg")
	try:
		int_value = int(sys.argv[index], base)
		return int_value
	except:
		printMessage(ERROR, "invalid argument: " + sys.argv[index], "getIntArg")

def getFloatArg(index, total_argument_number):
	if not checkArgumentExists(index):
		printMessage(ERROR, "not enough arguments: " + str(total_argument_number) + " arguments required", "getFloatArg")
	try:
		float_value = float(sys.argv[index])
		return float_value
	except:
		printMessage(ERROR, "invalid argument: " + sys.argv[index], "getFloatArg")

def getBoolArg(index, total_argument_number):
	if not checkArgumentExists(index):
		printMessage(ERROR, "not enough arguments: " + str(total_argument_number) + " arguments required", "getFloatArg")
	return sys.argv[index].upper() == "TRUE"

#file operations
def getFileLines(file_name):
	if not os.path.exists(file_name):
		printMessage(ERROR, file_name + " does not exist", "getFileLines")
	ftr = open(file_name, read_mode)
	lines = ftr.readlines()
	ftr.close()
	return lines

def getFileContent(file_name):
	if not os.path.exists(file_name):
		printMessage(ERROR, file_name + " does not exist", "getFileContent")
	ftr = open(file_name, read_mode)
	content = ftr.read()
	ftr.close()
	return content

def writeArrayToFile(file_name, array, mode = write_mode):
	if mode != write_mode or mode != append_mode:
		printMessage(ERROR, "invalid mode", "writeArrayToFile")
	if not type(array) is ListType:
		printMessage(ERROR, "invalid array", "writeArrayToFile")
	ftw = open(file_name, mode)
	for element in array:
		ftw.write(str(element) + EOL)
	ftw.close()

def appendArrayToFile(file_name, array):
	writeArrayToFile(file_name, array, append_mode)