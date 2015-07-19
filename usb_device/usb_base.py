import usb.core
import usb.util

class XDEV:
	def __init__(self, VENDOR_ID, PRODUCT_ID):
		self.VENDOR_ID = VENDOR_ID
		self.PRODUCT_ID = PRODUCT_ID

mouseReceiver = XDEV(0x045e, 0x0745)
keyboard = XDEV(0x045e, 0x00dd)
dataTraveler = XDEV(0x0930, 0x6545)
dvbStick = XDEV(0x2013, 0x024f)

item2search = dvbStick

# find our device
dev = usb.core.find(idVendor=item2search.VENDOR_ID, idProduct=item2search.PRODUCT_ID)

# was it found?
if dev is None:
    raise ValueError('Device not found')
print "device OK"
print dev
# set the active configuration. With no arguments, the first
# configuration will be the active one

NUM_OF_KERNEL_DRIVER = 5
#kernel detach
for i in range(NUM_OF_KERNEL_DRIVER):
	if dev.is_kernel_driver_active(i):
		print "kernel driver active", i
		dev.detach_kernel_driver(i)
print "kernel detach OK"

# get an endpoint instance
cfg = dev.get_active_configuration()
print "configuration get OK"
print cfg
interface_number = cfg[(0,0)].bInterfaceNumber
print "interface get OK"
print interface_number

intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number
    #bAlternateSetting = alternate_setting
)
print "interface find OK"
print intf



ep = usb.util.find_descriptor(intf)
print "endpoint find OK"
print ep
print ep.device
print ep.interface
print ep.index
'''
data = "OK"
ep.write(data)
print "ep write OK"
'''
read = ep.read(1)
print "ep read OK"
print "read data: " + str(read)

