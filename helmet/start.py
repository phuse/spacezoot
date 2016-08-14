#!/usr/bin/env python

import datetime
import time
from random import randint
delay = 1

from microdotphat import write_string, set_decimal, clear, show
from neopixel import *
# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# functions from rpi_ws2812 by jgaff/adafruit 
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

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

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
def fire(strip):
  	r = 74
  	g = 150
  	b = 12;

  //  Flicker, based on our initial RGB values
  	for i in range (0, strip.numPixels(), 1): 
    		int flicker = randint(0,55)
    		int r1 = r-flicker
    		int g1 = g-flicker
    		int b1 = b-flicker
    		if(g1<0): 
			g1=0
    		if(r1<0): 
			r1=0
    		if(b1<0): 
			b1=0
    		strip.setPixelColor(i,r1,g1, b1)
  
  	strip.show()

if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print ('Press Ctrl-C to quit.')
	while True:
		# Color wipe animations.
		colorWipe(strip, Color(255, 0, 0))  # Red wipe
		clear()
    		write_string("CPU:", kerning=False)
    		show()
    		time.sleep(delay)
		colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		clear()
    		path="/sys/class/thermal/thermal_zone0/temp"
    		f = open(path, "r")
    		temp_raw = int(f.read().strip())
    		temp = float(temp_raw / 1000.0)
    		write_string( "%.2f" % temp + "c", kerning=False)
    		show()
		colorWipe(strip, Color(0, 0, 255))  # Green wipe
    		time.sleep(delay)
		# Theater chase animations.
		#theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		#theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		#rainbow(strip)
                fire(strip)
		#rainbowCycle(strip)
		#theaterChaseRainbow(strip)
