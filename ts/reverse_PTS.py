import sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

PTS = getIntArg(1, 1)

data4 = ((PTS & 0x00000007F) << 1) | 0x1
data3 = (PTS & 0x000007F80) >> 7
data2 = ((PTS & 0x0003F8000) >> 14) | 0x1
data1 = (PTS & 0x03FC00000) >> 22
data0 = ((PTS & 0x1C0000000) >> 29) | 0x21

print hex(data0)[2:], hex(data1)[2:], hex(data2)[2:], hex(data3)[2:], hex(data4)[2:]
data0 = data0 | 0x31
print hex(data0)[2:], hex(data1)[2:], hex(data2)[2:], hex(data3)[2:], hex(data4)[2:]
