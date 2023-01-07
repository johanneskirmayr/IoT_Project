import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

broker = "broker.hivemq.com"

roomTopic = "iotlab/jj/rooms"
commandTopic = "iotlab/jj/commands"

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))

def on_message(client, userdata, message):
	time.sleep(1.0)
	print("received message =",str(message.payload.decode("utf-8")))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

print("Attempting to connect to broker " + broker)
client.connect(broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
client.loop_start()
client.subscribe(roomTopic)
client.subscribe(commandTopic)

while True:
    time.sleep(2.0)