#!/usr/bin/env python
import paho.mqtt.client as mqtt
import datetime
import time
from random import randint
delay = 2
silence = 10
lastmsgat = time.time()

from microdotphat import set_col,write_string, set_decimal, clear, show

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

# shows a random graph:
def graphz(seconds):
    graph = []
    filled = True

    t_end = time.time() + seconds
    while time.time() < t_end:
      clear()
      graph += [randint(0,7)]
      while len(graph) > 45:
        graph.pop(0)

      for x, val in enumerate(graph):
        if filled:
            set_col(x + (45-len(graph)), [
                0,
                0b1000000,
                0b1100000,
                0b1110000,
                0b1111000,
                0b1111100,
                0b1111110,
                0b1111111][val])
        else:
            set_col(x, 1 << (7-val))

      show()
      sleep(0.05)
     
# shows the clock
def showtime(seconds):
    t_end = time.time() + seconds
    while time.time() < t_end:
      clear()
      t = datetime.datetime.now()
      if t.second % 2 == 0:
        set_decimal(2, 1)
        set_decimal(4, 1)
       else:
        set_decimal(2, 0)
        set_decimal(4, 0)
       write_string(t.strftime('%H%M%S'), kerning=False)
      show()
      time.sleep(0.05)
    clear()
    lastmsgat = time.time()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global lastmsgat
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("helmet/#")
    clear()
    write_string('active', kerning=False)
    show()
    time.sleep(delay)
    lastmsgat = time.time()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lastmsgat
    print(msg.topic+" "+str(msg.payload))
    clear()
    write_string(remove_prefix(msg.topic, 'helmet/'), kerning=False)
    show()
    time.sleep(delay)
    clear()
    write_string(str(msg.payload), kerning=False)
    show()
    lastmsgat = time.time()
    time.sleep(delay)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
while True:
  client.loop()
  now = time.time()
  if now - lastmsgat > silence:
      print (datetime.datetime.fromtimestamp(now).strftime('%H:%M:%S') + " chirp")
      showtime(10);
      

