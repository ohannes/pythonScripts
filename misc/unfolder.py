import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

UNKNOWN_EXTENSION_GROUP = "other"

def changeCurrentWorkingDirectory(directory):
	for i in range(len(os.getcwd().split(PATH_SPLITTER)) - 1):
		os.chdir(PARENT_DIR)
	if not os.path.exists(directory):
		printMessage(ERROR, directory + " does not exist!", changeCurrentWorkingDirectory)
	os.chdir(directory)

def moveFiles2ParentDir(fileList):
	for fileName in fileList:
		if os.path.isdir(fileName):
			dirlist = os.listdir(fileName)
			os.chdir(fileName)
			moveFiles2ParentDir(dirlist)
			os.chdir('..')
		elif os.path.isfile(fileName):
			if os.path.exists(PARENT_DIR + PATH_SPLITTER + fileName):
				printMessage(WARNING, fileName + " exists in the " + fileExtension + " directory...", "moveFiles2ParentDir")
				printMessage(WARNING, "new file has been copied as " + DUPLICATE_NAME_SIGN + fileName, "moveFiles2ParentDir")
				os.rename(fileName, DUPLICATE_NAME_SIGN + fileName)
				os.system(COPY_CMD + PARAMETER_SPLITTER + DUPLICATE_NAME_SIGN + fileName + PARAMETER_SPLITTER + PARENT_DIR + PATH_SPLITTER + DUPLICATE_NAME_SIGN + fileName)
			else:
				os.system(COPY_CMD + PARAMETER_SPLITTER + fileName + PARAMETER_SPLITTER + PARENT_DIR + PATH_SPLITTER + fileName)

path = getStrArg(1, 1)
changeCurrentWorkingDirectory(path)
dirlist = os.listdir(os.getcwd())
moveFiles2ParentDir(dirlist)