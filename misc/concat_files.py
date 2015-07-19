si_path = "/home/arcelik/Documents/ROMEO/download/Contents/TS/Rohde&Schwarz/2013_06_03/TSanalyze_of_SyncTest_DVB_2e3.trp/"
pat = "pid0"
pmt = "pid32"
file_extesion = ".trp"
video = "input00"
output = "deneme"
si_frequency = 100
write_mode = "w"
END = "END"
TS_PACKET_SIZE = 188

pat_file_name = si_path + pat + file_extesion
pmt_file_name = si_path + pmt + file_extesion
video_file_name = video + file_extesion

pat_file = open(pat_file_name)
pmt_file = open(pmt_file_name)
video_file = open(video_file_name)

video_packets = video_file.read()

ftw = open(output + file_extesion, write_mode)

for i in range(len(video_packets)/TS_PACKET_SIZE):
	if not (i % si_frequency):
		pat_packet = pat_file.read(TS_PACKET_SIZE)
		pmt_packet = pmt_file.read(TS_PACKET_SIZE)
		ftw.write(pat_packet + pmt_packet)
	for j in range(TS_PACKET_SIZE):
		ftw.write(video_packets[i * TS_PACKET_SIZE + j])
pat_file.close()
pmt_file.close()
video_file.close()
ftw.close()