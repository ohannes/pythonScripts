TS_PACKET_LEN = 188
filter_pid_list = [0, 16, 17, 18, 19, 20, 32, 1001, 2002, 8191]

stream_file = "/home/arcelik/Desktop/stream.trp"

ftr = open(stream_file)
#stream = ftr.read()

number_of_packets = len(stream) / TS_PACKET_LEN

dvb_file = "/home/arcelik/Desktop/filtered.trp"
ftw = open(dvb_file, "w")
'''
for i in range(number_of_packets):
	packet = stream[i*TS_PACKET_LEN:(i+1)*TS_PACKET_LEN]
	pid = (ord(packet[1]) & 0x1F) * 0x100 + ord(packet[2])
	if pid in filter_pid_list:
		ftw.write(packet)
'''
while True:
	packet = ftr.read(TS_PACKET_LEN)
	if not packet:
		break
	pid = (ord(packet[1]) & 0x1F) * 0x100 + ord(packet[2])
	if pid in filter_pid_list:
		ftw.write(packet)

ftr.close()
ftw.close()
