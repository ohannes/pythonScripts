import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *

def getNumberOfLines(file_list, number_of_lines, number_of_files):
	for file_name in file_list:
		if os.path.isdir(file_name):
			os.chdir(file_name)
			getNumberOfLines(os.listdir(os.getcwd()), number_of_lines, number_of_files)
			os.chdir("..")
		else:
			if not ".svn-base" in file_name:
				lines = getFileLines(file_name)
				number_of_lines += len(lines)
				number_of_files += 1
				print len(lines), "lines in", file_name
	return number_of_lines, number_of_files

path = getStrArg(1, 1);
if not os.path.exists(path):
	printMessage(ERROR, "path " + path + " does not exists", "find_number_of_lines")
os.chdir(path)
number_of_lines, number_of_files = getNumberOfLines(os.listdir(os.getcwd()), 0, 0)

print number_of_lines, "lines in", number_of_files, "files"