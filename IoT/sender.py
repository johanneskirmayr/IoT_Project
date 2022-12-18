import time
import random
import string
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

broker = "test.mosquitto.org"

pub_topic = "iotlab/jj/test"

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))
	
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

print("Attempting to connect to broker " + broker)
client.connect(broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
client.loop_start()

def random_letter():
    return random.choices(string.ascii_uppercase, k=1)

client.publish(pub_topic, "START")

while True:
    data = random_letter()
    #client.publish(pub_topic, str(data[0]))
    time.sleep(2.0)