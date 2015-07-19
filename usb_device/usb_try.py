import usb.core
import usb.util

VENDOR_ID = 0x2013
PRODUCT_ID = 0x024f

# find our device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)

print ep

exit(1)

# was it found?
if dev is None:
    raise ValueError('Device not found')
print "device found: " + "vendor id: " + str(dev.idVendor) + " product id: " + str(dev.idProduct)

dev.set_configuration()
print "configuration OK!"

for cfg in dev:
	print "configuration: " + str(cfg.bConfigurationValue) + '\n'
	for intf in cfg:
		print '\t' + "interface: " + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n'
		for ep in intf:
			print '\t\t' + "endpoint: " + str(hex(ep.bEndpointAddress)) + '\n'
			msg = 'test'
			print '\t\t' + "test message: " + msg
			#dev.write(ep.bEndpointAddress, msg, intf.bInterfaceNumber)
			#print '\t\t' + "write: " + msg
			ret = dev.read(ep.bEndpointAddress, len(msg), 0, 100)
			sret = ''.join([chr(x) for x in ret])
			print '\t\t' + "read: " + sret
			assert sret == msg
			print '\t\t' + "r/w OK! " + "configuration: " + str(cfg.bConfigurationValue) + " interface: " + str(intf.bInterfaceNumber) + " endpoint: " + str(hex(ep.bEndpointAddress))



'''
# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_settting = usb.control.get_interface(interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
    bAlternateSetting = alternate_setting
)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)

assert ep is not None

# write the data
ep.write('test')
'''
