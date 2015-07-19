import os
import sys

TEMP_FILE = "compileAppTemp"
execS = "[exec]"
errorS = "error(s)"
warningS = "warning(s)"
totalTime = "Total time"

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

def similiarTo(string):
	falseString = "false"
	falseCNT = 0
	trueString = "true"
	trueCNT = 0
	if string == falseString:
		return falseString
	if string == trueString:
		return trueString
	for char in falseString:
		if char in string:
			falseCNT += 1
	for char in trueString:
		if char in string:
			trueCNT += 1
	if trueCNT > falseCNT:
		return trueString
	return falseString

def changeCurrentWorkingDirectory(directory):
	for i in range(len(os.getcwd().split("/")) - 1):
		os.chdir("..")
	if not os.path.exists(directory):
		print "ERROR: " + directory + " does not exist!"
		exit(1)
	os.chdir(directory)

confFileName = "/home/arcelik/pythonScripts/web_app/pythonScripts.conf"

if len(sys.argv) == 1:
	print "ERROR: no appplication has been selected to be compiled!"
	exit(1)
elif len(sys.argv) == 2:
	APP_NAME = sys.argv[1]
	ENABLE_DEBUG = "false"
else:
	if seemsLikeConfigure(sys.argv[1]):
		setConfiurePath(sys.argv[2])
		print "new src path has been set as", sys.argv[2]
		exit(1)
	APP_NAME = sys.argv[1]
	ENABLE_DEBUG = similiarTo(sys.argv[2])
	if sys.argv[2] != "true" or sys.argv[2] != "false":
		print "WARNING: debug=" + ENABLE_DEBUG + " assumed!"

confFile = open(confFileName, "r")
splitted = confFile.readline().split("=")
if len(splitted) != 2:
	print "ERROR: in configuration file", confFileName
	confFile.close()
	exit(1)
srcPath = splitted[1]
confFile.close()

changeCurrentWorkingDirectory(srcPath)

compileString = "ant -Dname=" + APP_NAME + " -Ddebug=" + ENABLE_DEBUG + " build"

if os.path.exists(srcPath + "/widgets/" + APP_NAME):
	print "START: compile started..."
	os.system(compileString + " > " + TEMP_FILE)
else:
	print "ERROR: " + srcPath + APP_NAME + " does not exist!"
	exit(1)

tempFile = open("compileAppTemp", "r")
tempLines = tempFile.readlines()
tempFile.close()
os.remove("compileAppTemp")

numOfError = ""
numOfWarn = ""
rateOfType = ""

for line in tempLines:
	if "error(s)" in line and "warning(s)" in line and "typed" in line:
		split = line.split()
		for i in range(len(split)):
			if "error(s)" in split[i]:
				errorNumBulk = split[i-1]
				j = -1
				while True:
					try:
						temp = int(errorNumBulk[j])
						numOfError = numOfError + errorNumBulk[j]
					except:
						break
					if j + len(errorNumBulk) == 0:
						break
					j -= 1
				numOfError = int(numOfError)
				numOfWarn = int(split[i+1])
				rateOfType = split[i+3]
				break

if numOfError > 0:
	print "ERROR: compile failed!"
elif numOfWarn > 0:
	print "WARNING!"
else:
	print "SUCCESS: compile finished!"
	print numOfError, "error(s)", numOfWarn, "warning(s)", rateOfType, "typed"

if numOfError + numOfWarn > 0:
	print "\n"
	for line in tempLines:
		print line

if numOfError == 0:
	indexPath = "widgets/" + APP_NAME + "/WebContent/"
	os.chdir(indexPath)
	os.system("chromium-browser --disable-web-security --allow-file-access-from-files index.html")