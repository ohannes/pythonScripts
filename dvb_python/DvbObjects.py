import linuxdvb, fcntl, ctypes, time, os, threading

ADAPTER_PATH = "/dev/dvb/adapter"
ADAPTER_NUM = 0
FE_NUM = 0
DVR_NUM = 0
DMX_NUM = 0
TS_PACKET_SIZE = 188
TS_PACKET_BUFFER_SIZE_AS_PACKETS = 1000
TS_PACKET_BUFFER_SIZE_AS_BYTES = TS_PACKET_BUFFER_SIZE_AS_PACKETS * TS_PACKET_SIZE
NUMBER_OF_PACKETS_PER_READ = 5

def printPacket(packet):
	packet_str = ""
	for byte in packet:
		packet_str += str(hex(ord(byte)))[2:] + " "
	print packet_str

class DvbSubdeviceTypes:
	dvb_frontend = 0
	dvb_demux = 1
	dvb_dvr = 2

class EsSourceTypes:
	es_source_dvb = 0
	es_source_p2p = 1

class EsTypes:
	es_all = 0
	es_video = 1
	es_audio = 2
	es_private_data = 3

class EsSubtypes:
	es_base = 0
	es_enhancement = 1

class DvbParams:
	def __init__(self, frequency, bandwidth, code_rate_HP, code_rate_LP, inversion, constellation, transmission_mode, guard_interval, hierarchy_information):
		self.frequency = frequency * 1000
		self.bandwidth = bandwidth
		self.code_rate_HP = code_rate_HP
		self.code_rate_LP = code_rate_LP
		self.inversion = inversion
		self.constellation = constellation
		self.transmission_mode = transmission_mode
		self.guard_interval = guard_interval
		self.hierarchy_information = hierarchy_information

	def printAttributes(self):
		print "frequency:", self.frequency
		print "bandwidth:", self.bandwidth
		print "code_rate_HP:", self.code_rate_HP
		print "code_rate_LP:", self.code_rate_LP
		print "inversion:", self.inversion
		print "constellation:", self.constellation
		print "transmission_mode:", self.transmission_mode
		print "guard_interval:", self.guard_interval
		print "hierarchy_information:", self.hierarchy_information

class FeInfo:
 	def __init__(self, fd):
 		self.fd = fd

 		self.info = linuxdvb.dvb_frontend_info()
 		fcntl.ioctl(fd, linuxdvb.FE_GET_INFO, self.info)
 		
		self.name = self.info.name
		self.fe_type = self.convertFeType()
		self.frequency_min = self.info.frequency_min
		self.frequency_max = self.info.frequency_max
		self.frequency_stepsize = self.info.frequency_stepsize
		self.frequency_tolerance = self.info.frequency_tolerance
		self.symbol_rate_min = self.info.symbol_rate_min
		self.symbol_rate_max = self.info.symbol_rate_max
		self.symbol_rate_tolerance = self.info.symbol_rate_tolerance
		self.notifier_delay = self.info.notifier_delay

	def convertFeType(self):
		if self.info.type == linuxdvb.FE_QAM:
			return "DVB-C"
		elif self.info.type == linuxdvb.FE_QPSK:
			return "DVB-S"
		elif self.info.type == linuxdvb.FE_OFDM:
			return "DVB-T"
		elif self.info.type == linuxdvb.FE_ATSC:
			return "ATSC", feinfo.type
		else:
			return "UNKNOWN"

	def printAttributes(self):
		print "name:", self.name
		print "fe_type:", self.fe_type
		print "frequency_min:", self.frequency_min
		print "frequency_max:", self.frequency_max
		print "frequency_stepsize:", self.frequency_stepsize
		print "frequency_tolerance:", self.frequency_tolerance
		print "symbol_rate_min:", self.symbol_rate_min
		print "symbol_rate_max:", self.symbol_rate_max
		print "symbol_rate_tolerance:", self.symbol_rate_tolerance
		print "notifier_delay:", self.notifier_delay

class FeStatus:
	def __init__(self, fd):
		self.fd = fd

		self.has_signal = False
		self.has_carrier = False
		self.has_viterbi = False
		self.has_sync = False
		self.has_lock = False
		self.timedout = True
		self.reinit = True

		self.reset()

	def reset(self):
		status = ctypes.c_uint()
		fcntl.ioctl(self.fd, linuxdvb.FE_READ_STATUS, status)

		if status.value & linuxdvb.FE_HAS_SIGNAL:
			self.has_signal = True
		else:
			self.has_signal = False

		if status.value & linuxdvb.FE_HAS_CARRIER:
			self.has_carrier = True
		else:
			self.has_carrier = False

		if status.value & linuxdvb.FE_HAS_VITERBI:
			self.has_viterbi = True
		else:
			self.has_viterbi = False

		if status.value & linuxdvb.FE_HAS_SYNC:
			self.has_sync = True
		else:
			self.has_sync = False

		if status.value & linuxdvb.FE_HAS_LOCK:
			self.has_lock = True
		else:
			self.has_lock = False

		if status.value & linuxdvb.FE_TIMEDOUT:
			self.timedout = True
		else:
			self.timedout = False

		if status.value & linuxdvb.FE_REINIT:
			self.reinit = True
		else:
			self.reinit = False

	def isTuned(self):
		return self.has_signal and self.has_sync and self.has_lock

	def printAttributes(self):
		print "has_signal:", self.has_signal
		print "has_carrier:", self.has_carrier
		print "has_viterbi:", self.has_viterbi
		print "has_sync:", self.has_sync
		print "has_lock:", self.has_lock
		print "timedout:", self.timedout
		print "reinit:", self.reinit

class FeParams:
	def __init__(self, fd, dvb_parameters):
		self.fd = fd
		self.dvb_parameters = dvb_parameters

		self.params = linuxdvb.dvb_frontend_parameters()
		self.params.frequency = self.dvb_parameters.frequency
		self.params.u.ofdm.bandwidth = self.dvb_parameters.bandwidth
		self.params.u.ofdm.code_rate_HP = self.dvb_parameters.code_rate_HP
		self.params.u.ofdm.code_rate_LP = self.dvb_parameters.code_rate_LP
		self.params.inversion = self.dvb_parameters.inversion
		self.params.u.ofdm.constellation = self.dvb_parameters.constellation
		self.params.u.ofdm.transmission_mode = self.dvb_parameters.transmission_mode
		self.params.u.ofdm.guard_interval = self.dvb_parameters.guard_interval
		self.params.u.ofdm.hierarchy_information = self.dvb_parameters.hierarchy_information
		
		self.reset()

	def reset(self):
		fcntl.ioctl(self.fd, linuxdvb.FE_SET_FRONTEND, self.params)

	def printAttributes(self):
		print "frequency:", self.dvb_parameters.frequency
		print "bandwidth:", self.dvb_parameters.bandwidth
		print "code_rate_HP:", self.dvb_parameters.code_rate_HP
		print "code_rate_LP:", self.dvb_parameters.code_rate_LP
		print "inversion:", self.dvb_parameters.inversion
		print "constellation:", self.dvb_parameters.constellation
		print "transmission_mode:", self.dvb_parameters.transmission_mode
		print "guard_interval:", self.dvb_parameters.guard_interval
		print "hierarchy_information:", self.dvb_parameters.hierarchy_information

class DmxPesFilter:
	def __init__(self, fd, pid, input_type, output_type, pes_type, flags):
		self.fd = fd
		self.pid = pid
		self.input = input_type
		self.output = output_type
		self.pes_type = pes_type
		self.flags = flags

		self.pes_filter = linuxdvb.dmx_pes_filter_params()
		self.pes_filter.fd = self.fd
		self.pes_filter.pid = self.pid
		self.pes_filter.input = self.input
		self.pes_filter.output = self.output
		self.pes_filter.pes_type = self.pes_type
		self.pes_filter.flags = self.flags

		fcntl.ioctl(self.fd, linuxdvb.DMX_SET_PES_FILTER, self.pes_filter)

	def printAttributes(self):
		print "pid:", self.pid
		print "input:", self.input
		print "output:", self.output
		print "pes_type:", self.pes_type
		print "flags:", self.flags

class DvbSubdevice:
	def __init__(self, adapter_num, subdevice_num, subdevice_type):
		self.fd = -1
		self.adapter_num = adapter_num
		self.subdevice_num = subdevice_num
		self.subdevice_type = subdevice_type

	def getSubDeviceName(self):
		if self.subdevice_type == DvbSubdeviceTypes.dvb_frontend:
			return "frontend"
		if self.subdevice_type == DvbSubdeviceTypes.dvb_demux:
			return "demux"
		if self.subdevice_type == DvbSubdeviceTypes.dvb_dvr:
			return "dvr"
		return "unknown"

	def Xopen(self, flags):
		path = ADAPTER_PATH + str(self.adapter_num) + "/" + self.getSubDeviceName() + str(self.subdevice_num)
		if os.path.exists(path):
			temp = open(path, flags)
			if temp >= 0:
				self.fd = temp
			else:
				print "device could not be opened", path
		else:
			print "device path does not exist", path
	
	def Xclose(self):
		if self.fd >= 0:
			close(self.fd)

	def openRD(self):
		self.Xopen("r+")

	def openRB(self):
		self.Xopen("rb")

	def openRDWR(self):
		self.Xopen("w+")

	def isDeviceOpen(self):
		return self.fd >= 0

class FeDevice(DvbSubdevice):
	def __init__(self, adapter_num, subdevice_num):
		DvbSubdevice.__init__(self, adapter_num, subdevice_num, DvbSubdeviceTypes.dvb_frontend)
		self.openRDWR()
		self.info = None
		self.params = None
		self.status = None

	def tune(self, dvb_parameters, timeout):
		print "tuning..."
		if not self.isDeviceOpen():
			print "tune failed"
			return False
		self.info = FeInfo(self.fd)
		self.params = FeParams(self.fd, dvb_parameters)
		self.status = FeStatus(self.fd)
		if not self.waitUntilTuned(timeout):
			print "tune failed"
			return False
		print "tuned."
		return True

	def waitUntilTuned(self, timeout):
		if not self.isDeviceOpen():
			return False
		self.status.reset()
		tune_time = 0
		while not self.status.has_lock:
			tune_time += 1
			if tune_time == timeout * 100:
				print "tuning timeout..."
				return False
			self.status.reset()
		return True

class DmxDevice(DvbSubdevice):
	def __init__(self, adapter_num, subdevice_num):
		DvbSubdevice.__init__(self, adapter_num, subdevice_num, DvbSubdeviceTypes.dvb_demux)
		self.openRDWR()
		self.pes_filter = None

	def setPesFilter(self, pid, input_type, output_type, pes_type, flags):
		if not self.isDeviceOpen():
			return
		self.pes_filter = DmxPesFilter(self.fd, pid, input_type, output_type, pes_type, flags)

class DvrDevice(DvbSubdevice):
	def __init__(self, adapter_num, subdevice_num, num_of_packets_per_read):
		DvbSubdevice.__init__(self, adapter_num, subdevice_num, DvbSubdeviceTypes.dvb_dvr)
		
		self.buffer = []
		self.num_of_packets_per_read = num_of_packets_per_read
		self.num_of_packets_read = 0
		self.num_of_packets_serviced = 0
		self.read_size = 0
		self.openRB()

	def receivePacket(self):
		if not self.isDeviceOpen():
			return None
		if ctypes.get_errno() == 75: #EOVERFLOW
			print "OVERFLOW in dvr buffer!"
			return None

		while self.read_size <= 0:
			self.buffer = self.fd.read(TS_PACKET_SIZE * self.num_of_packets_per_read)
			self.read_size = TS_PACKET_SIZE * self.num_of_packets_per_read
			self.num_of_packets_read = self.read_size / TS_PACKET_SIZE

		if self.num_of_packets_serviced < self.num_of_packets_read:
			self.num_of_packets_serviced += 1
			start_index = (self.num_of_packets_serviced - 1) * TS_PACKET_SIZE
			end_index = start_index + TS_PACKET_SIZE
			return self.buffer[start_index:end_index]
		else:
			self.num_of_packets_serviced = 0
			self.read_size = 0
			self.num_of_packets_read = 0
			return self.receivePacket()

class ReceiveTsPacketsThread(threading.Thread):
	def __init__(self, receiver):
		threading.Thread.__init__(self)
		self.receiver = receiver

	def run(self):
		print "receiver", self.receiver.receiver_id, "ReceiveTsPacketsThread started"
		while True:
			self.receiver.writePacket()
			if self.receiver.must_stop:
				break
		print "receiver", self.receiver.receiver_id, "ReceiveTsPacketsThread stopped"

class PrepareTsFramesThread(threading.Thread):
	def __init__(self, receiver):
		threading.Thread.__init__(self)
		self.receiver = receiver

	def run(self):
		print "receiver", self.receiver.receiver_id, "PrepareTsFramesThread started"
		while True:
			self.receiver.readPacket()
			if self.receiver.must_stop:
				break
		print "receiver", self.receiver.receiver_id, "PrepareTsFramesThread stopped"

class PrepareTsEnhancedFramesThread(threading.Thread):
	def __init__(self, receiver):
		threading.Thread.__init__(self)
		self.receiver = receiver

	def run(self):
		print "receiver", self.receiver.receiver_id, "PrepareTsEnhancedFramesThread started"
		while True:
			self.receiver.prepareFrame()
			if self.receiver.must_stop:
				break
		print "receiver", self.receiver.receiver_id, "PrepareTsEnhancedFramesThread stopped"

class SendTsEnhancedFramesThread(threading.Thread):
	def __init__(self, receiver):
		threading.Thread.__init__(self)
		self.receiver = receiver

	def run(self):
		print "receiver", self.receiver.receiver_id, "SendTsEnhancedFramesThread started"
		while True:
			self.receiver.sendFrame()
			if self.receiver.must_stop:
				break
		print "receiver", self.receiver.receiver_id, "SendTsEnhancedFramesThread stopped"

class TsReceiverBase:
	def __init__(self, source, index, r_type, subtype):
		self.ts_packet_buffer_current_size = 0
		self.write_offset = 0
		self.read_offset = 0
		self.is_sending = False
		self.source = source
		self.index = index
		self.type = r_type
		self.subtype = subtype
		self.conf_file = None
		self.ts_packet_buffer = []
		self.sending_frame_flag = False
		self.mutex = threading.Lock()
		self.receive_ts_packets_thread = None
		self.prepare_ts_frames_thread = None
		self.prepare_ts_enhanced_frames_thread = None
		self.send_ts_enhanced_frames_thread = None
		self.must_stop = False
		self.receiver_id = "r" + str(self.source) + str(self.index) + str(self.type) + str(self.subtype)

	def lock(self):
		self.mutex.acquire()

	def release(self):
		self.mutex.release()

	def writePacket(self):
		while self.ts_packet_buffer_current_size == TS_PACKET_BUFFER_SIZE_AS_PACKETS:
			time.sleep(0.000001)
		packet = self.receivePacket()
		if packet != None:
			self.ts_packet_buffer[(self.write_offset):(self.write_offset + TS_PACKET_SIZE)] = packet
			self.write_offset = (self.write_offset + TS_PACKET_SIZE) % TS_PACKET_BUFFER_SIZE_AS_BYTES
			self.lock()
			self.ts_packet_buffer_current_size += 1
			self.release()
		else:
			print "receiver", self.receiver_id, "received empty packet"
			self.stopThreads()

	def readPacket(self):
		while self.ts_packet_buffer_current_size <= 0:
			time.sleep(0.000001)
		packet = self.ts_packet_buffer[(self.read_offset):(self.read_offset + TS_PACKET_SIZE)]
		self.read_offset = (self.read_offset + TS_PACKET_SIZE) % TS_PACKET_BUFFER_SIZE_AS_BYTES
		self.lock()
		self.ts_packet_buffer_current_size -= 1
		self.release()
		#printPacket(packet)
		return packet

	def tune(self):
		pass

	def receivePacket(self):
		pass

	def prepareFrame(self):
		pass

	def getFirstPTS():
		pass

	def syncByPTS(PTS):
		pass

	def sendFrame(self):
		pass

	def start2receiveTsPackets(self):
		self.receive_ts_packets_thread = ReceiveTsPacketsThread(self)
		self.receive_ts_packets_thread.start()

	def start2prepareTsFrames(self):
		self.prepare_ts_frames_thread = PrepareTsFramesThread(self)
		self.prepare_ts_frames_thread.start()

	def start2prepareTsEnhancedFrames(self):
		self.prepare_ts_enhanced_frames_thread = PrepareTsEnhancedFramesThread(self)
		self.prepare_ts_enhanced_frames_thread.start()

	def start2sendTsEnhancedFrames(self):
		self.send_ts_enhanced_frames_thread = SendTsEnhancedFramesThread(self)
		self.send_ts_enhanced_frames_thread.start()

	def tuned(self):
		self.start2receiveTsPackets()
		self.start2prepareTsFrames()

	def stopThreads(self):
		self.must_stop = True
		#self.receive_ts_packets_thread._stop()
		#self.prepare_ts_frames_thread._stop()
		#self.prepare_ts_enhanced_frames_thread._stop()
		#self.send_ts_enhanced_frames_thread._stop()

class TsReceiverDVB(TsReceiverBase):
	def __init__(self):
		TsReceiverBase.__init__(self, EsSourceTypes.es_source_dvb, 0, EsTypes.es_all, EsSubtypes.es_base)
		self.fe = FeDevice(ADAPTER_NUM, FE_NUM)
		self.dvr = DvrDevice(ADAPTER_NUM, DVR_NUM, NUMBER_OF_PACKETS_PER_READ)
		self.dmx = DmxDevice(ADAPTER_NUM, DMX_NUM)

	def tune(self, dvb_parameters, timeout):
		if self.fe.tune(dvb_parameters, timeout):
			self.dmx.setPesFilter(0x2000, linuxdvb.DMX_IN_FRONTEND, linuxdvb.DMX_OUT_TS_TAP, linuxdvb.DMX_PES_OTHER, linuxdvb.DMX_IMMEDIATE_START)
			self.tuned()
			return True
		return False
			
	def receivePacket(self):
		return self.dvr.receivePacket()

dvb_parameters = DvbParams(482000, linuxdvb.BANDWIDTH_8_MHZ, linuxdvb.FEC_AUTO, linuxdvb.FEC_AUTO, linuxdvb.INVERSION_AUTO, linuxdvb.QAM_64, linuxdvb.TRANSMISSION_MODE_8K, linuxdvb.GUARD_INTERVAL_AUTO, linuxdvb.HIERARCHY_NONE)
ts_receiver_dvb = TsReceiverDVB()
if ts_receiver_dvb.tune(dvb_parameters, 5):
	print "receiver", ts_receiver_dvb.receiver_id, "is working..."
else:
	print "receiver", ts_receiver_dvb.receiver_id, "could not tune."

while True:
	user_input = raw_input()
	if "exit" in user_input:
		ts_receiver_dvb.stopThreads()
		break