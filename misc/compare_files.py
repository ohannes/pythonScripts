import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *

file_name1 = getStrArg(1, 2)
file_name2 = getStrArg(2, 2)

lines1 = getFileLines(file_name1)
lines2 = getFileLines(file_name2)

if len(lines1) != len(lines2):
	sys.exit("number of lines are not equal")

for i in range(len(lines1)):
	if len(lines1[i]) != len(lines2[i]):
		print len(lines1[i]), len(lines2[i])
		#sys.exit("line " + str(i+1) + " lengths are not equal")
		print "line " + str(i+1) + " lengths are not equal"
	minimum_length = min(len(lines1[i]), len(lines2[i]))
	for j in range(minimum_length):
		if lines1[i][j] != lines2[i][j]:
			print lines1[i][j], lines2[i][j]
			sys.exit("line " + str(i+1) + " character " + str(j+1) + " are not the same")

sys.exit("Completely the same")
