import usb.core
import usb.util

VENDOR_ID = 0x0930
PRODUCT_ID = 0x6545

# find our device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

# was it found?
if dev is None:
    raise ValueError('Device not found')
print "device OK"
print dev
# set the active configuration. With no arguments, the first
# configuration will be the active one
'''
dev.set_configuration()
print "configuration set OK"
'''
# get an endpoint instance
cfg = dev.get_active_configuration()
print "configuration get OK"
print cfg
interface_number = cfg[(0,0)].bInterfaceNumber
print "interface get OK"
print interface_number
'''
alternate_setting = usb.control.get_interface(dev, interface_number)
print "alternate get OK"
print alternate_setting
'''
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number
    #bAlternateSetting = alternate_setting
)
print "interface find OK"
print intf
'''
ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)
'''
'''
dev.detach_kernel_driver(interface_number)
print "detach kernel OK"
'''
ep = usb.util.find_descriptor(intf)
print "endpoint find OK"
print ep
print ep.device
print ep.interface
print ep.index
data = "OK"
ep.write(data)
print "ep write OK"
read = ep.read(1)
print "ep read OK"
print "read data: " + str(read)

