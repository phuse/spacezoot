#!/usr/bin/env python
import paho.mqtt.client as mqtt
import datetime
import time
from random import randint
delay = 2

from microdotphat import write_string, set_decimal, clear, show

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("helmet/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    clear()
    write_string(remove_prefix(msg.topic, 'helmet/'), kerning=False)
    show()
    time.sleep(delay)
    clear()
    write_string(str(msg.payload), kerning=False)
    show()
    time.sleep(delay)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
