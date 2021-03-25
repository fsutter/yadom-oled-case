#!/usr/bin/env python3

import os
import time
import sys
import socket
import fcntl
import struct

# OLED screen
import board
import digitalio
import adafruit_ssd1306

# buttons
import RPi.GPIO as GPIO

# offscreen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
oled_reset = digitalio.DigitalInOut(board.D25)
oled_cs = digitalio.DigitalInOut(board.CE0)
oled_dc = digitalio.DigitalInOut(board.D24)

# 128x64 display with hardware SPI:
spi = board.SPI()
width = 128
height = 64
oled = adafruit_ssd1306.SSD1306_SPI(width, height, spi, oled_dc, oled_reset, oled_cs)

# buttons 
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)  # SW1
GPIO.setup(17, GPIO.IN) # SW2
GPIO.setup(18, GPIO.IN) # SW4
GPIO.setup(27, GPIO.IN) # SW3

# This sets TEXT equal to whatever your IP address is, or isn't
def ip_address():
        try:
                TEXT = get_ip_address(b'wlan0') # WiFi address of WiFi adapter. NOT ETHERNET
        except IOError:
                try:
                        TEXT = get_ip_address(b'eth0') # WiFi address of Ethernet cable. NOT ADAPTER
                except IOError:
                        TEXT = ('NO INTERNET!')
        return TEXT

# This function allows us to grab any of our IP addresses
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new('1', (width, height))
padding = 2
top = padding
bottom = height - padding
x = padding

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

# Load fonts
smallFont = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'Xerox Serif Narrow.ttf'), 14)
largeFont = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'Xerox Serif Narrow.ttf'), 20)
bigFont = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'Xerox Serif Narrow.ttf'), 28)

mode = 0
switchDecounter = 0
lastString = ''
while True:
	if mode == 0: # display date and time
		str1 = time.strftime("%A")
		str2 = time.strftime("%X")
		str3 = time.strftime("%e %b %Y")
		if (str1 + str2 + str3) != lastString:
			draw.rectangle((0,0,width,height), outline=0, fill=0)
			draw.text((padding, padding), str1,  font=smallFont, fill=255)
			sizeX, sizeY = draw.textsize(str2, font=bigFont)
			draw.text(((oled.width - sizeX) / 2, (oled.height - sizeY) / 2), str2,  font=bigFont, fill=255)
			sizeX, sizeY = draw.textsize(str3, font=smallFont)
			draw.text((oled.width - sizeX - padding, oled.height - sizeY - padding), str3,  font=smallFont, fill=255)
			oled.image(image)
			oled.show()
			lastString=str1 + str2 + str3
	elif mode == 1: # display time
		str2 = time.strftime("%X")
		if str2 != lastString:
			draw.rectangle((0,0,width,height), outline=0, fill=0)
			sizeX, sizeY = draw.textsize(str2, font=bigFont)
			draw.text(((oled.width - sizeX) / 2, (oled.height - sizeY) / 2), str2,  font=bigFont, fill=255)
			oled.image(image)
			oled.show()
			lastString=str2
	elif mode == 2: # display IP address
		str1='IP address'
		str2=ip_address()
		print(str2)
		if (str1 + str2) != lastString:
			draw.rectangle((0,0,width,height), outline=0, fill=0)
			size1X, size1Y = draw.textsize(str1, font=largeFont)
			size2X, size2Y = draw.textsize(str2, font=largeFont)
			draw.text(((oled.width - size1X) / 2, (oled.height - (size1Y + size2Y + padding)) / 2), str1,  font=largeFont, fill=255)
			draw.text(((oled.width - size2X) / 2, (oled.height - (size1Y + size2Y + padding)) / 2 + padding + size1Y), str2,  font=largeFont, fill=255)
			oled.image(image)
			oled.show()
			lastString=str1 + str2
	if not GPIO.input(4): # SW1 - IP
		mode = 2
	elif not GPIO.input(17) : # SW2 - Date and time
		mode = 0
	elif not GPIO.input(18) : # SW4 - Time
		mode = 1
	elif not GPIO.input(27) : # SW3 - rotate not more often as once per second if button is held
		if switchDecounter == 0:
			if mode < 2:
				mode = mode + 1
			else:
				mode = 0
			switchDecounter = 10
		else:
			switchDecounter -= 1
	else:
		switchDecounter = 0 # reset as button is not held
	time.sleep(0.1)

