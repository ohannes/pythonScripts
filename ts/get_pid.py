SYNC_BYTE = 71
TS_PACKET_LEN = 188

input_file = "audio.ts"
output_file = "output"

ftr = open(input_file, "rb")
content =  ftr.read()
ftr.close()

if len(content) % TS_PACKET_LEN != 0:
	print "ERROR: number of bytes is not a multiple of 188"

print "content length:", len(content) / TS_PACKET_LEN
pids = []

pid0_cnt = 0
pid66_cnt = 0
pid68_cnt = 0

def print_packet(index):
	i = 0
	packet = ""
	while i < 188:
		e = str(hex(ord(content[index+i])))[2:]
		if len(e) == 1:
			e = "0" + e
		packet += e
		if i != 187:
			if len(e) == 1:
				packet += "  "
			elif len(e) == 2:
				packet += " "
		i += 1
	print packet

def get_byte(index, byte):
	return ord(content[index+byte])

i=0
while i < len(content):
	byte0 = ord(content[i+0])
	byte1 = ord(content[i+1])
	byte2 = ord(content[i+2])
	byte3 = ord(content[i+3])
	byte4 = ord(content[i+4])
	
	sync_byte = byte0
	transport_error_indicator = ((byte1 & 0x80) >> 7)
	payload_unit_start_indicator = ((byte1 & 0x40) >> 6)
	transport_priority = ((byte1 & 0x20) >> 5)
	pid = ((byte1 & 0x1F) * 0x100) + byte2
	transport_scrambling_control = ((byte3 & 0xC0) >> 6)
	adaptation_field_control = ((byte3 & 0x30) >> 4)
	continuity_counter = (byte3 & 0x0F)
	if adaptation_field_control == 0x03:
		adaptation_field_len = byte4

	if sync_byte != SYNC_BYTE:
		print "ERROR: sync byte not found"
		print_packet(i)
	
	if not pid in pids:
		pids.append(pid)
		print "a packet with new pid:", pid
		if adaptation_field_control == 0x03:
			print "adaptation_field_len:", adaptation_field_len
		print_packet(i)

	if pid == 0:
		pid0_cnt += 1
	elif pid == 66:
		pid66_cnt += 1
	elif pid == 68:
		pid68_cnt += 1
	else:
		print "ERROR: unexpected pid:", pid
	
	i += 188

for pid in pids:
	print pid

print "number of packets with pid 0 is", pid0_cnt
print "number of packets with pid 66 is", pid66_cnt
print "number of packets with pid 68 is", pid68_cnt


