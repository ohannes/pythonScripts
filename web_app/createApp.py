import os
import sys

def seemsLikeConfigure(string):
	confString = "configure"
	if string == confString or string[0:4] == confString[0:4]:
		return True
	return False

def setConfiurePath(path):
	global confFileName
	if not os.path.exists(path):
		print "ERROR:", path, "is not an existing directory"
		exit(1)
	confFile = open(confFileName, "w")
	confFile.write("srcPath=" + path)
	confFile.close()

def isFile(fileName):
	if "." in fileName:
		return True
	return False

def replaceTemplateWithNew(fileList):
	for fileName in fileList:
		if "svn" in fileName:
			continue
		if isFile(fileName):
			fileContent = getFileContent(fileName)
			newContent = fileContent.replace(TEMPLATE_APP, NEW_APP)
			newFileName = fileName.replace(TEMPLATE_APP, NEW_APP)
			os.rename(fileName, newFileName)
			try:
				ftw = open(newFileName, "w")
			except:
				print "ERROR: file could not be opened...", newFileName
				exit(1)
			ftw.write(newContent)
		else:
			fileList = os.listdir(fileName)
			os.chdir(fileName)
			replaceTemplateWithNew(fileList)
			os.chdir('..')

def changeCurrentWorkingDirectory(directory):
	for i in range(len(os.getcwd().split("/")) - 1):
		os.chdir("..")
	os.chdir(directory)

def getFileContent(fileName):
	try:
		ftr = open(fileName, "r")
	except:
		print "ERROR: file could not be opened...", fileName
		exit(1)
	fileContent = ftr.read()
	ftr.close()
	return fileContent

confFileName = "/home/arcelik/pythonScripts/web_app/pythonScripts.conf"

if len(sys.argv) == 1:
	print "ERROR: no applicatio name has been entered!"
	exit(1)
elif len(sys.argv) == 2:
	NEW_APP = sys.argv[1]
else:
	if seemsLikeConfigure(sys.argv[1]):
		setConfiurePath(sys.argv[2])
		print "new src path has been set as", sys.argv[2]
		exit(1)

TEMPLATE_APP = "template"

confFile = open(confFileName, "r")
splitted = confFile.readline().split("=")
if len(splitted) != 2:
	print "ERROR: in configuration file", confFileName
	confFile.close()
	exit(1)
SRC_ROOT = splitted[1]
confFile.close()

API_DIR = "/libraries/api/"
WIDGET_DIR = "/widgets/"
JS_DIR = "/WebContent/js/"
MSAPIjs = "MSAPI.js"

try:
	changeCurrentWorkingDirectory(SRC_ROOT + WIDGET_DIR)
except:
	print "ERROR: src root doesn't exist...", SRC_ROOT + WIDGET_DIR
	exit(1)

if os.path.exists(SRC_ROOT + WIDGET_DIR + NEW_APP):
	print "WARNING: The old " + NEW_APP + " will be removed!"
	print "Press 'Y/y' to continue or any key to exit..."
	userChoice = raw_input()
	if userChoice == "" or userChoice.upper() != 'Y':
		print "creating new application has been cancelled."
		exit(1)
	else:
		os.system("rm -rf " + NEW_APP)
		print "The old " + NEW_APP + " has been removed!"

os.system("cp -r " + TEMPLATE_APP + " " + NEW_APP)

try:
	fileList = os.listdir(NEW_APP)
except:
	print "ERROR: template widget doesn't exist..."
	exit(1)

os.chdir(NEW_APP)
replaceTemplateWithNew(fileList)

try:
	changeCurrentWorkingDirectory(SRC_ROOT + API_DIR)
except:
	print "ERROR: src root doesn't exist..."
	exit(1)

if os.path.exists(SRC_ROOT + WIDGET_DIR + NEW_APP):
	os.system("rm -rf " + NEW_APP)

os.system("cp -r " + TEMPLATE_APP + " " + NEW_APP)

try:
	fileList = os.listdir(NEW_APP)
except:
	print "ERROR: template api doesn't exist..."
	exit(1)

os.chdir(NEW_APP)
replaceTemplateWithNew(fileList)

changeCurrentWorkingDirectory(SRC_ROOT + WIDGET_DIR + NEW_APP + JS_DIR)
if os.path.exists(MSAPIjs):
	os.remove(MSAPIjs)

print "SUCCESS: new application has been created..."
