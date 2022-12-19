# Create a class called MQTTClient that will be used to send and receive messages from the broker. 
# The class will have the following methods: send_message, receive_message, and connect.

from paho.mqtt import client as mqtt_client
from queue import Queue


class MQTTClient:
    def __init__(self):
        # Create a client instance
        self.client = mqtt_client.Client()
        # Create a queue to store received messages
        self.message_queue = Queue()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        # Set the callback function
        self.client.on_connect = on_connect
        
        # Set broker
        self.broker = "test.mosquitto.org"

        # Connect to the broker
        self.client.connect(self.broker)

        return self.client

    def send_message(self, topic, message):
        # Send a message to the broker
        result = self.client.publish(topic, message)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def receive_message(self, topic):
        # Receive a message from the broker
        self.client.subscribe(topic)
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_message(self, client, userdata, message):
        # Callback function for when a message is received
        self.message_queue.put(message.payload.decode('utf-8'))
        # print("Received message '" + str(message.payload) + "' on topic '"
        #       + message.topic + "' with QoS " + str(message.qos))