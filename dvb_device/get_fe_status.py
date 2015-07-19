import linuxdvb
import fcntl

fefd = open('/dev/dvb/adapter0/frontend0', 'r+')
feinfo = linuxdvb.dvb_frontend_info()
fcntl.ioctl(fefd, linuxdvb.FE_GET_INFO, feinfo)

print feinfo.name

'''
for bit, flag in linuxdvb.fe_caps.items():
     if (feinfo.caps & bit) > 0:
         print flag
'''
fefd.close()

fefd_ = open('/dev/dvb/adapter0/frontend0', 'w+')

params = linuxdvb.dvb_frontend_parameters()
params.frequency = 482 * 1000 * 1000
params.u.ofdm.bandwidth = linuxdvb.BANDWIDTH_8_MHZ
params.u.ofdm.code_rate_HP = linuxdvb.FEC_NONE
params.u.ofdm.code_rate_LP = linuxdvb.FEC_2_3
params.inversion = linuxdvb.INVERSION_AUTO
params.u.ofdm.constellation = linuxdvb.QAM_16
params.u.ofdm.transmission_mode = linuxdvb.TRANSMISSION_MODE_8K
params.u.ofdm.guard_interval = linuxdvb.GUARD_INTERVAL_1_8
params.u.ofdm.hierarchy_information = linuxdvb.HIERARCHY_NONE

fcntl.ioctl(fefd_, linuxdvb.FE_SET_FRONTEND, params)

params_ = linuxdvb.dvb_frontend_parameters()

status = linuxdvb.fe_status()

fcntl.ioctl(fefd_, linuxdvb.FE_READ_STATUS, status)

print "FE_HAS_SIGNAL: ", (status & linuxdvb.FE_HAS_SIGNAL)
print "FE_HAS_CARRIER: ", (status & linuxdvb.FE_HAS_CARRIER)
print "FE_HAS_VITERBI: ", (status & linuxdvb.FE_HAS_VITERBI)
print "FE_HAS_SYNC: ", (status & linuxdvb.FE_HAS_SYNC)
print "FE_HAS_LOCK: ", (status & linuxdvb.FE_HAS_LOCK)
print "FE_TIMEDOUT: ", (status & linuxdvb.FE_TIMEDOUT)
print "FE_REINIT: ", (status & linuxdvb.FE_REINIT)
