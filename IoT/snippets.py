# ======== Beacon detection with pygatt ===========
#from pygatt import BluetoothLEDevice
import pygatt
#from pygatt import BLEDevice

# 1. This script should discover BLE beacons, 
# 2. check if it is a beacon, 
# 3. and if yes print out uuid, major and minor value

# 1.Discover BLE beacons
scanner = pygatt.GATTToolBackend()
scanner.start()
#devices = scanner.scan()
#devices = scanner.scan(timeout=10)
devices = scanner.scan(timeout=10, run_as_root=True)
for device in devices:
    # 2. Check if it is a beacon
    #print(device.address)
    # 3. If yes print out uuid, major and minor value


    print(device)
    #print("Detected device %s" % device)

# for device in devices:
#     if device.address == <beacon's MAC address>:
#         print("Found beacon with MAC address:", device.address)
#         device.connect()
#         data = device.char_read("<characteristic UUID>")
#         print("Received data from beacon:", data)