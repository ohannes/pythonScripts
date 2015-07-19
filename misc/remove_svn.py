import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

def removeSVNfiles(file_list):
	for file_name in file_list:
		if os.path.isdir(file_name) and file_name == ".svn":
			try:
				os.system("rm -rf " + file_name)
			except:
				printMessage(ERROR, file_name + " could not be removed", "removeSVNfiles")
			continue
		if os.path.isdir(file_name):
			os.chdir(file_name)
			removeSVNfiles(os.listdir(os.getcwd()))
			os.chdir('..')

path = getStrArg(1, 1)
if path[0] != "/":
	path = os.getcwd() + "/" + path
if not os.path.exists(path):
	printMessage(ERROR, path + " does not exist.", "remove_svn")
os.chdir(path)
removeSVNfiles(os.listdir(os.getcwd()))