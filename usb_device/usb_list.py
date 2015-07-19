import usb
vendor_ids = []
product_ids = []
busses = usb.busses()
for bus in busses:
  devices = bus.devices
  for dev in devices:
    #_name = usb.util.get_string(dev.dev,256,2)  #This is where I'm having trouble
    #print "device name=",_name
    print "Device:", dev.filename
    print "  Device class:",dev.deviceClass
    print "  Device sub class:",dev.deviceSubClass
    print "  Device protocol:",dev.deviceProtocol
    print "  Max packet size:",dev.maxPacketSize
    print "  idVendor:",hex(dev.idVendor)
    print "  idProduct:",hex(dev.idProduct)
    if not hex(dev.idVendor) in vendor_ids:
      vendor_ids.append(hex(dev.idVendor))
      product_ids.append([])
    product_ids[vendor_ids.index(hex(dev.idVendor))].append(hex(dev.idProduct))
    print "  Device Version:",dev.deviceVersion
    for config in dev.configurations:
      print "  Configuration:", config.value
      print "    Total length:", config.totalLength 
      print "    selfPowered:", config.selfPowered
      print "    remoteWakeup:", config.remoteWakeup
      print "    maxPower:", config.maxPower
      for intf in config.interfaces:
        print "    Interface:",intf[0].interfaceNumber
        for alt in intf:
          print "    Alternate Setting:",alt.alternateSetting
          print "      Interface class:",alt.interfaceClass
          print "      Interface sub class:",alt.interfaceSubClass
          print "      Interface protocol:",alt.interfaceProtocol
          for ep in alt.endpoints:
            print "      Endpoint:",hex(ep.address)
            print "        Type:",ep.type
            print "        Max packet size:",ep.maxPacketSize
            print "        Interval:",ep.interval

print "\n\nSummary:"
print"\n"
for i in range(len(vendor_ids)):
  print "vendor id:", vendor_ids[i]
  for j in range(len(product_ids[i])):
    print "\tproduct id:", product_ids[i][j]