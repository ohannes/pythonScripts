import os, sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

def getBits(b, s, c):
	if c <= 0:
		printMessage(ERROR, "count cannot be negative or zero", "getBits")
	if s < 0:
		printMessage(ERROR, "start cannot be negative", "getBits")
	bin_array = bin(b)[2:]
	bin_length = len(bin_array)
	if c + s > bin_length:
		printMessage(ERROR, "not enough bits", "getBits")
	result_bin_array = ""
	i = 0
	while len(result_bin_array) < c:
		if i >= s:
			result_bin_array += bin_array[-i-1]
		i += 1
	return int(result_bin_array[::-1], 2)

b = getIntArg(1, 3)
s = getIntArg(2, 3)
c = getIntArg(3, 3)

print getBits(b, s, c)
