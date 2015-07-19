import sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

data0 = getIntArg(1, 5, 16)
data1 = getIntArg(2, 5, 16)
data2 = getIntArg(3, 5, 16)
data3 = getIntArg(4, 5, 16)
data4 = getIntArg(5, 5, 16)

pts1 = (data0 & 0x0E) >> 1
marker = data0 & 0x01
if marker != 1:
	print "ERROR: first marker bit is not 1"

pts2 = (data1 << 7) | ((data2 & 0xFE) >> 1)
marker = data0 & 0x01
if marker != 1:
	print "ERROR: second marker bit is not 1"

pts3 = (data3 << 7) | ((data4 & 0xFE) >> 1)
marker = data0 & 0x01
if marker != 1:
	print "ERROR: third marker bit is not 1"

PTS = (pts1 << 30) | (pts2 << 15) | pts3;
print "PTS value:", PTS
