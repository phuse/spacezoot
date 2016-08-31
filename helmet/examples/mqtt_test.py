#!/usr/bin/env python

#Libraries we need

#paho is a client, mosquitto must be running, since it is the broker. check.
import paho.mqtt.client as mqtt

#To be able to listen to keypress events. This will be replaced by whatever asynchronous events the raspi nano can handle
import pyxhook
import time

#to make client object visible to kbevent
client = mqtt.Client()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# client.subscribe("knappar/")
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

#This function is called every time a key is presssed
def kbevent( event ):
	#print key info
	print(event)
	client.publish("roevhatt_mqtt", str(event))
	#If the ascii value matches spacebar, terminate the while loop
	if event.Ascii == 32:
		global running
		running = False


client.connect("192.168.43.170", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message


## This is just to get keyboard events
#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
#Hook the keyboard
hookman.HookKeyboard()
#Start our listener
hookman.start()

#Create a loop to keep the application running
#running = True
#while running:
#	time.sleep(0.1)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_forever()

#Close the keyboad listener when we are done
hookman.cancel()

