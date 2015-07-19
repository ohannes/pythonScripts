import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

def removeSpacesFromEOL(fileName):
	lines = getFileLines(fileName)
	try:
		ftw = open(fileName, "w")
	except:
		printMessage(ERROR, "ERROR: no permission to write to " + fileName, "removeSpacesFromEOL")
	for line in lines:
		i = -1
		newLine = ""
		while i + len(line) != -1:
			if line[i] != " " and line[i] != "\t" and line[i] != "\n":
				break
			i -= 1
		newLine = line[0:len(line)+i+1] + "\n"
		newLine = newLine.replace(" ;", ";")
		ftw.write(newLine)
	ftw.close()

def checkFileList(files):
	for fileName in files:
		if '.svn' in fileName:
			return
		if os.path.isfile(fileName):
			removeSpacesFromEOL(fileName)
		else:
			fileList = os.listdir(fileName)
			os.chdir(fileName)
			checkFileList(fileList)
			os.chdir('..')

path = getStrArg(1, 1)
if not os.path.exists(path):
	printMessage(ERROR, path + " does not exist.", "remove_spaces")
os.chdir(path)
checkFileList(os.listdir(os.getcwd()))