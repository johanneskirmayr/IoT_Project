# IoT_Project

## Description:
The aim is to call a drone at the entrance of the building by pressing a button. The drone then guides him to his desired destination. On the way, the drone explains the rooms and important information about the building to the visitor by voice. The rooms are equipped with Low-Energy Bluetooth (BT) beacons which get detected by the drone. By calling a drone at the entrance of the building and guiding visitors to their desired destination, we aim to make the process of finding one’s way around the building more efficient and stress-free. The project goals were to build a minimal setup of the described task. This includes the setup of virtual Bluetooth beacons, to detect the beacons with a python script on a Raspberry Pi, and to trigger voice messages based on the detected UUID of the BT beacon which are read out via a speaker. Furthermore, we aimed to develop an Android application that communicates with the Raspberry Pi via MQTT and therefore lets the user call a drone, displays the current location with the beacons as waypoints, and has an emergency stop. Our project does not include an actual drone and navigation of the drone but focuses on the communication between the Raspberry Pi (on the drone) with the BT beacons and the Android app.

## Usage:
- Install the needed packages (see below)
- Run the script `beacon.py` on the Raspberry Pi which is the main file with:
```
sudo python3 beacon.py
```
(sudo is needed to access to Bluetooth)

### Other scripts:
- `sender.py`: publishes a specified message to the specified topic to the MQTT broker; 
Usage: 
```sudo python3 sender.py <message> <topic>```
- `receiver.py`: subscribes to a topic and prints the received messages; Usage: specify the topic in the script and run it with 
```sudo python3 receiver.py```

## Hardware:
- Raspberry Pi with Bluetooth and WiFi
- Bluetooth beacons (physical or simulated with a smartphone)
- Loudspeaker

# Nedded packages:
- bluepy (to detect BLE devices) - not available for Windows

Install with:
```pip install bluepy```

- paho-mqtt (to communicate with the MQTT broker)

Install with:
```pip install paho-mqtt```

- gtts (Google's Text to Speech API)

Install with:
```pip install gTTS```

- playsound (to play the audio file)

Install with:
```pip install playsound```
