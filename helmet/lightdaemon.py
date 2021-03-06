import time
import RPi.GPIO as GPIO
from daemonize import Daemonize

pid = "/tmp/test.pid"


from neopixel import *


# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#adjust for where your switch is connected
buttonPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def colorblink(strip, color, wait_s=1):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, 0)
	strip.setPixelColor(4, color)
	strip.show()
	time.sleep(wait_s)
	strip.setPixelColor(4, 0)
	strip.show()
	time.sleep(wait_s)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def main():
	# Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
    strip.begin()
	#adjust for where your switch is connected
    while True:
     input_state = GPIO.input(buttonPin)
     if input_state == False:
        colorblink(strip, Color(60, 60, 0)) # Green wipe
     else:
        colorWipe(strip, Color(200, 0, 100)) # Green wipe
        time.sleep(0.2)



daemon = Daemonize(app="test_app", pid=pid, action=main)
daemon.start()

