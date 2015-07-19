import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

applicationName = getStrArg(1, 1)

def getLocalStoreItem(line):
	keyStr = "window.localStorage"
	i = 0
	while True:
		if i == len(line):
			break
		if line[i:len(keyStr)+i] == keyStr:
			if not'"' in line[len(keyStr)+i:] and not "'" in line[len(keyStr)+i:]:
				return ""
			itemStr = ""
			while line[i] != "'" and line[i] != '"':
				i += 1
			i += 1
			while line[i] != "'" and line[i] != '"':
				itemStr += line[i]
				i += 1
			return itemStr
		i += 1

appPathList =	[
					"/home/arcelik/projects/apps/source/widgets/src/libraries/api/" + applicationName,
					"/home/arcelik/projects/apps/source/widgets/src/widgets/" + applicationName + "/javascript",
					"/home/arcelik/projects/apps/source/widgets/src/widgets/" + applicationName + "/WebContent/js"
				]

localStoreStr = "window.localStorage.setItem"
lines = []
items = []

for appPath in appPathList:
	try:
		dirList = os.listdir(appPath)
	except:
		print "ERROR: incorrect application path"
		exit(1)
	for fileName in dirList:
		lines += getFileLines(appPath + "/" + fileName)

for line in lines:
	if localStoreStr in line:
		item = getLocalStoreItem(line)
		if not item in items and item != "":
			items.append(item)

for item in items:
	print item


