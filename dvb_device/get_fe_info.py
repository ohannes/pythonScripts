import linuxdvb
import fcntl

fepath = '/dev/dvb/adapter0/frontend0'
fefd = open(fepath, 'r+')
feinfo = linuxdvb.dvb_frontend_info()
fcntl.ioctl(fefd, linuxdvb.FE_GET_INFO, feinfo)

'''
print feinfo.name

for bit, flag in linuxdvb.fe_caps.items():
	if (feinfo.caps & bit) > 0:
		print(flag)
'''

if feinfo.type == linuxdvb.FE_QAM:
	print "DVB-C"
elif feinfo.type == linuxdvb.FE_QPSK:
	print "DVB-S"
elif feinfo.type == linuxdvb.FE_OFDM:
	print "DVB-T"
elif feinfo.type == linuxdvb.FE_ATSC:
	print "ATSC", feinfo.type
else:
	print "unknown type", feinfo.type, "for frontend", fepath

fefd.close()
