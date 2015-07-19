import usb
import usb.core

VENDOR_ID = 0x2013
PRODUCT_ID = 0x024f
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
dev.set_configuration()
print "configuration OK"
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(dev, interface_number)
intf = usb.util.find_descriptor(cfg, bInterfaceNumber=interface_number, bAlternateSetting = alternate_setting)
ep = usb.util.find_descriptor(intf, )
print "ep found"
test_read = ep.read()
#test_read = dev.read(0x81,1)
print "read as test from usb: ", test_read
