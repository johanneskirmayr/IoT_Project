import os
from bluepy.btle import Scanner
import uuidDatabank
import mqttConnect 
from gtts import gTTS
import playsound
import time
import sys
import subprocess

# Create list of already detected UUIDs
detected_uuids = []

# Create main fucntion to run the program
def main():
    """
    Main function: continously scans the BT devices nearby, and triggers voice message if new UUID is found
    """
    # Check if start button is pressed on app
    started = False
    stopped = False

    # Define topics
    roomTopic = "iotlab/jj/rooms"
    commandTopic = "iotlab/jj/commands"

    # Connect to MQTT broker
    mqtt = mqttConnect.MQTTClient()
    client = mqtt.connect()

    uuidData = uuidDatabank.DataBank()

    # Subscribe to topic via MQTT
    mqtt.receive_message(roomTopic)
    mqtt.receive_message(commandTopic) 

    # Check if start button is pressed on app
    while not started:
        # Check if "start" is in the message queue
        # mqtt.receive_message(commandTopic)
        while not mqtt.message_queue_commands.empty():
            message = mqtt.message_queue_commands.get()
            # Remove the message from the queue
            if message == "START":
                print("Scanner started!")
                started = True
                time.sleep(2) # there needs to be a small delay, so the app can catch the "START" command
                client.publish(commandTopic, "START")

                # get the destination room from the topic room message queue
                if not mqtt.message_queue_rooms.empty():
                    destination_room = mqtt.message_queue_rooms.get()
                    # Remove the message from the queue
                    print("Destination room: " + destination_room)
                else: 
                    print("No destination room found")
                    destination_room = None

                # Get the waypoints the user has to pass to get to the destination room
                waypoints = uuidData.get_way(destination_room)

                #TODO: check if correct
                # Delete all entrys of uuidData.databank that are not in the waypoints list
                for uuid in uuidData.databank:
                    if uuid not in waypoints:
                        del uuidData.databank[uuid]

                break

    while not stopped:
        try:
            # Create a scanner object
            scanner = Scanner()
            # Scan for devices
            devices = scanner.scan(timeout=10, passive=True) 

            # Loop through all the devices found
            for device in devices:
                # Extract the UUID from the data
                uuid = extract_uuid(device.getScanData())
                #print all the data detailed


                # Check if the UUID is already detected
                if uuid in detected_uuids and uuid != None:
                    # If already detected, skip
                    continue
                elif uuid != None:
                    # If not detected, add to the list
                    # Check if the UUID is in the databank
                    if uuid in uuidData.databank:
                        # Add the UUID to the list of detected UUIDs
                        detected_uuids.append(uuid)

                        # Get the data of the UUID
                        location = uuidData.get_location(uuid)
                        floor = location["floor"]
                        room = location["room"]
                        voice_message = location["voice_message"]
                        
                        print("Detected new Bluetooth beacon of room: " + str(room))
                        # Get the bridge voice message of the next waypoint
                        if uuid in waypoints:
                            # get the index of the uuid in the waypoints list
                            index = waypoints.index(uuid)

                            # check if the uuid is the last waypoint
                            if index != 0:
                                # add the bridge voice message of the next element in the list to the voice message
                                bridge_message = uuidData.get_location(waypoints[index-1])["bridge_voice_message"]
                                voice_message = voice_message + bridge_message
                        
                        if room == destination_room:
                            voice_message = voice_message + "You have arrived at your destination. Thank you for using the tour guide! Have a nice day!"
                        # Play the voice message 
                        tts = gTTS(text=voice_message, lang='en')
                        #print("Saving audiofile!")
                        tts.save("voice_message.mp3")
                        #print("Playing audiofile!")
                        playsound.playsound("voice_message.mp3")
                        #Delete the file after playing
                        #print("Removing audiofile!")
                        os.remove("voice_message.mp3")

                        #Publish detected UUID via MQTT to the Android app
                        client.publish(roomTopic, room)

                        #TODO: check if correct
                        # If the room is the destination room, reset the tour and publish RESET
                        if room == destination_room:
                            client.publish(commandTopic, "RESET")
                            stopped = True
                            print("Tour reset!")
                            # Call the script again
                            subprocess.call([sys.executable, "beacon.py"])
                            sys.exit()

            # Check if "RESET" is in the message queue
            # mqtt.receive_message(commandTopic)
            while not mqtt.message_queue_commands.empty():
                message = mqtt.message_queue_commands.get()
                # Remove the message from the queue
                if message == "RESET":
                    stopped = True
                    print("Tour reset!")
                    # Call the script again
                    subprocess.call([sys.executable, "beacon.py"])
                    sys.exit()
                
        except KeyboardInterrupt:
            # Stop scanning if CTRL-C is pressed
            print("Scanning stopped")
            break

# Function to extract the UUID from the data
def extract_uuid(data):
    newData = data[0]
    _, _, value = newData
    # Extract the UUID from the data
    try:
        uuid = value[8:40]
        return uuid
    except:
        return None
    # Return the UUID

# Run the main function
if __name__ == "__main__":
    main()
