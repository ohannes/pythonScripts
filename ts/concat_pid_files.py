import sys, os, time

TS_PACKET_SIZE = 188
file_extension = ".trp"
pat_pid = 0
pmt_pid = 32
base_video_pid = 1001 #default ?
video_pid = 1001 #default ?
if len(sys.argv) > 1:
	video_pid = int(sys.argv[1], 10)
else:
	print "default video pid:", video_pid
	#sys.exit("argument missing: video pid")

byte1 = ((base_video_pid | 0xE000) >> 8);
byte2 = (base_video_pid & 0x00FF);

#print "byte 1:", hex(byte1), byte1
#print "byte 2:", hex(byte2), byte2

stream_file_name = "stream" + str(video_pid) + file_extension

stream_file = open(stream_file_name, "w")

print "reading PAT file"
pat_file = open("pid" + str(pat_pid) + file_extension)
pat_packet = pat_file.read(TS_PACKET_SIZE)
pat_file.close()
print "reading PAT file END"

print "reading PMT file"
pmt_file = open("pid" + str(pmt_pid) + file_extension)
pmt_packet = pmt_file.read(TS_PACKET_SIZE)
#pmt_packet = ""
#for i in range(len(_pmt_packet)):
#	if i == 13 or i == 18:
#		pmt_packet += chr(byte1)
#	elif i == 14 or i == 19:
#		pmt_packet += chr(byte2)
#	else:
#		pmt_packet += _pmt_packet[i]
pmt_file.close()
print "reading PMT file END"

print "reading VIDEO file"
video_file = open("pid" + str(video_pid) + file_extension)
_video_stream = video_file.read()
video_stream = ""
for i in range(len(_video_stream)):
	if i % TS_PACKET_SIZE == 2:
		video_stream += chr(byte2)
	else:
		video_stream += _video_stream[i]
#i = 0
#while i < len(video_stream):
#	print str(hex(ord(video_stream[0+i]))), str(hex(ord(video_stream[1+i]))), str(hex(ord(video_stream[2+i]))), str(hex(ord(video_stream[3+i])))
#	i += TS_PACKET_SIZE
video_file.close()
print "reading VIDEO file END"

print "writing PAT"
stream_file.write(pat_packet)
print "writing PAT END"
print "writing PMT"
stream_file.write(pmt_packet)
print "writing PMT END"
print "writing VIDEO"
stream_file.write(video_stream)
print "writing VIDEO END"

stream_file.close()

time.sleep(1)

#os.system("vlc " + stream_file_name)
