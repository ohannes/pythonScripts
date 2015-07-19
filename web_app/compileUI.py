import os
import sys 

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

def getEnableDebug():
	if len(sys.argv) == 1:
		ENABLE_DEBUG = "false"
		print "WARNING: debug=" + ENABLE_DEBUG + " assumed!"
	else:
		ENABLE_DEBUG = similiarTo(sys.argv[1])
		if sys.argv[1] != "true" or sys.argv[1] != "false":
			print "WARNING: debug=" + ENABLE_DEBUG + " assumed!"
	return ENABLE_DEBUG

def compileCss():
	global APP_NAME
	frameList = os.listdir("libraries/webui/frames")
	targetCssFile = open("widgets/" + APP_NAME + "/WebContent/css/ky_ui.css", "w")
	for frame in frameList:
		if os.path.isdir("libraries/webui/frames/" + frame):
			frameFiles = os.listdir("libraries/webui/frames/" + frame)
			for frameFile in frameFiles:
				if frameFile.split(".")[-1] == "css":
					cssFile = open("libraries/webui/frames/" + frame + "/" + frameFile, "r")
					cssContent = cssFile.read()
					cssFile.close()
					targetCssFile.write(cssContent)
	#targetCssFile.close()
	
	popupList = os.listdir("libraries/webui/popups")
	#targetCssFile = open("widgets/" + APP_NAME + "/WebContent/css/ky_ui.css", "w")
	for popup in popupList:
		if os.path.isdir("libraries/webui/popups/" + popup):
			popupFiles = os.listdir("libraries/webui/popups/" + popup)
			for popupFile in popupFiles:
				if popupFile.split(".")[-1] == "css":
					cssFile = open("libraries/webui/popups/" + popup + "/" + popupFile, "r")
					cssContent = cssFile.read()
					cssFile.close()
					targetCssFile.write(cssContent)
	targetCssFile.close()

APP_NAME = "ky_ui"

os.chdir("../../..")	#libraries folder

compileString = "ant -Dname=" + APP_NAME + " -Ddebug=" + getEnableDebug() + " build"

if os.path.exists("widgets/" + APP_NAME):
	print "START: compile started..."
	os.system(compileString + " > " + "compileAppTemp")
else:
	sys.exit("ERROR: " + APP_NAME + " does not exist under src/widgets!")

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
	compileCss()
	indexPath = "widgets/" + APP_NAME + "/WebContent/"
	os.chdir(indexPath)
	os.system("google-chrome --disable-web-security --allow-file-access-from-files index.html")
