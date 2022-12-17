from bluepy.btle import Scanner
import databank
import mqtt
from gtts import gTTS

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

    # Connect to MQTT broker
    mqtt = MQTTClient("client_id", "broker_ip", "broker_port") #TODO: fill in
    client = mqtt.connect()

    #TODO: check if correct
    # Subscribe to topic button via MQTT
    mqtt.receive_message("button") #TODO: fill in topic

    #TODO: check if correct
    while not started:
        # Check if "start" is in the message queue
        while not mqtt.message_queue.empty():
            message = mqtt.message_queue.get()
            # Remove the message from the queue
            mqtt.message_queue.pop()
            if message == "start":
                started = True
                break

    while not stopped:
        try:
            # Create a scanner object
            scanner = Scanner()
            # Scan for devices
            devices = scanner.scan(timeout=10, passive=True) # TODO: passive?

            # Loop through all the devices found
            for device in devices:
                # Extract the UUID from the advertisement data
                uuid = extract_uuid(device.getScanData())

                # Check if the UUID is already detected
                if uuid in detected_uuids:
                    # If already detected, skip
                    continue
                else:
                    # If not detected, add to the list
                                    # Check if the UUID is in the databank
                    if uuid in databank:
                        # Add the UUID to the list of detected UUIDs
                        detected_uuids.append(uuid)

                        # Get the data of the UUID
                        location = databank.get_data(uuid)
                        floor = location["floor"]
                        room = location["room"]
                        voice_message = location["voice_message"]
                        
                        # Play the voice message #TODO: look if it makes sense to directly trigger voice message or delay
                        tts = gTTS(text=voice_message, lang='en')
                        tts.play()

                        #TODO: publish detected UUID via MQTT to the Android app
                        client.publish("topic", uuid) #TODO: fill in topic


                        #TODO: check if detected UUID is the end beacon

            #TODO: check if correct
            # Check if "stop" is in the message queue
            while not mqtt.message_queue.empty():
                message = mqtt.message_queue.get()
                # Remove the message from the queue
                mqtt.message_queue.pop()
                if message == "stop":
                    stopped = True
                    break
                
        except KeyboardInterrupt:
            # Stop scanning if CTRL-C is pressed
            print("Scanning stopped")
            break
            #break

# Function to extract the UUID from the advertisement data
def extract_uuid(data):
    # Extract the UUID from the data
    uuid = data[9:25]
    # Return the UUID
    return uuid

# Run the main function
if __name__ == "__main__":
    main()
