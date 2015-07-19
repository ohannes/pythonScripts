import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

CREATE_DIR_CMD = "mkdir"
COPY_CMD = "mv"
PATH_SPLITTER = "/"
DUPLICATE_NAME_SIGN = "_"
PARENT_DIR = ".."
EXTENSION_SPLITTER = "."
UNKNOWN_EXTENSION_GROUP = "other"
PARAMETER_SPLITTER = " "
LAST_INDEX = -1
INIT_STR = ""

def changeCurrentWorkingDirectory(directory):
	for i in range(len(os.getcwd().split(PATH_SPLITTER)) - 1):
		os.chdir(PARENT_DIR)
	if not os.path.exists(directory):
		print "ERROR: " + directory + " does not exist!"
		exit(1)
	os.chdir(directory)


path = getStrArg(1, 1)
changeCurrentWorkingDirectory(path)
dirlist = os.listdir(os.getcwd())

for fileName in dirlist:
	if os.path.isdir(fileName):
		continue
	fileExtension = INIT_STR
	if  fileName[LAST_INDEX] != EXTENSION_SPLITTER and EXTENSION_SPLITTER in fileName:
		fileExtension = fileName.split(EXTENSION_SPLITTER)[LAST_INDEX]
	else:
		fileExtension = UNKNOWN_EXTENSION_GROUP
	if not os.path.exists(fileExtension):
		os.system(CREATE_DIR_CMD + PARAMETER_SPLITTER + fileExtension)
	if os.path.exists(fileExtension + PATH_SPLITTER + fileName):
		print "WARNING: " + fileName + " exists in the " + fileExtension + " directory..."
		print "WARNING: " + "new file has been copied as " + DUPLICATE_NAME_SIGN + fileName
		os.rename(fileName, DUPLICATE_NAME_SIGN + fileName)
		os.system(COPY_CMD + PARAMETER_SPLITTER + DUPLICATE_NAME_SIGN + fileName + PARAMETER_SPLITTER + fileExtension + PATH_SPLITTER + DUPLICATE_NAME_SIGN + fileName)
	else:
		os.system(COPY_CMD + PARAMETER_SPLITTER + fileName + PARAMETER_SPLITTER + fileExtension + PATH_SPLITTER + fileName)

