import sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

input_file = getStrArg(1, 1)
output_file = input_file + ".regulated"

lines = getFileLines(input_file)

ftw = open(output_file, write_mode)

for line in lines:
	sharp_found = False
	equal_found = False
	line_regulated = False
	if not "=>" in line or not "#" in line or not "_" in line:
		ftw.write(line)
		continue
	index = 0
	while True:
		if index == len(line) - 1:
			ftw.write(line[index])
			break
		if line[index] == "#":
			sharp_found = True
		if line[index] == "=" and line[index+1] == ">":
			equal_found = True
		if line[index] == "_" and (not sharp_found) and equal_found and (not line_regulated):
			ftw.write(line[index+1].upper())
			index += 1
			line_regulated = True
		else:
			ftw.write(line[index])
		index += 1

ftw.close()



