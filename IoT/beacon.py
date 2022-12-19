from bluepy.btle import Scanner
import uuidDatabank
import mqttConnect 
from gtts import gTTS
import time

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
    mqtt = mqttConnect.MQTTClient() #TODO: fill in
    client = mqtt.connect()

    uuidData = uuidDatabank.DataBank()

    #TODO: check if correct
    # Subscribe to topic via MQTT
    mqtt.receive_message(commandTopic) 

    #TODO: check if correct
    while not started:
        # Check if "start" is in the message queue
        # mqtt.receive_message(commandTopic)
        while not mqtt.message_queue.empty():
            message = mqtt.message_queue.get()
            # Remove the message from the queue
            if message == "START":
                print("Scanner started!")
                started = True
                time.sleep(2) # there needs to be a small delay, so the app can catch the "START" command
                client.publish(commandTopic, "START")
                break

    while not stopped:
        try:
            # Create a scanner object
            scanner = Scanner()
            # Scan for devices
            devices = scanner.scan(timeout=10, passive=True) # TODO: passive?

            # Loop through all the devices found
            for device in devices:
                # Extract the UUID from the data
                uuid = extract_uuid(device.getScanData())

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
                        
                        # Play the voice message #TODO: test if it makes sense to directly trigger voice message or delay
                        tts = gTTS(text=voice_message, lang='en')
                        print(voice_message)

                        #TODO: publish detected UUID via MQTT to the Android app
                        client.publish(roomTopic, room) 


                        #TODO: check if detected UUID is the end beacon

            # Check if "RESET" is in the message queue
            # mqtt.receive_message(commandTopic)
            while not mqtt.message_queue.empty():
                message = mqtt.message_queue.get()
                # Remove the message from the queue
                if message == "RESET":
                    stopped = True
                    print("Tour reset!")
                    break
                
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
