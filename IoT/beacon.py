from bluepy.btle import Scanner, ScanEntry

scanner = Scanner()
devices = scanner.scan(timeout=10, passive=True) # TODO: passive?

for device in devices:
    print("Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi))
    for (adtype, desc, value) in device.getScanData():
        print("  %s = %s" % (desc, value))
