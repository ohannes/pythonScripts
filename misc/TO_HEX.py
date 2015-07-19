import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *

inputFile = getStrArg(1, 2)
if not os.path.exists(inputFile):
	sys.exit("input file does not exist: " + inputFile)
output_file = inputFile + ".hex"
line_break_range = getIntArg(2, 2)
write_number_header = True
if len(sys.argv) > 3:
	write_number_header = getBoolArg(3, 2)

'''
content = getFileContent(inputFile)
print "content length:", len(content), "bytes"
for i in range(len(content)):
	str2write = str(hex(ord(content[i])))
	if not write_number_header:
		str2write = str2write[2:]
	ftw.write(str2write)
	if i != 0 and (i+1) % line_break_range == 0:
		ftw.write(EOL)
	else:
		ftw.write(SPACE)
ftw.close()
'''

ftw = open(output_file, write_mode)
ftr = open(inputFile)
bytes = ftr.read(line_break_range)
while bytes:
	for i in range(len(bytes)):
		str2write = str(hex(ord(bytes[i])))
		if not write_number_header:
			str2write = str2write[2:]
		ftw.write(str2write)
		if i != 0 and (i+1) % line_break_range == 0:
			ftw.write(EOL)
		else:
			ftw.write(SPACE)
	bytes = ftr.read(line_break_range)
ftw.close()