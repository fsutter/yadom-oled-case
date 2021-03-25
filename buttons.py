#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)  # SW1
GPIO.setup(17, GPIO.IN)  # SW2
GPIO.setup(18, GPIO.IN)  # SW4
GPIO.setup(27, GPIO.IN)  # SW3

while True:
    if not GPIO.input(4):
        print("SW1")
        # wait for button to be released
        while not GPIO.input(4):
            time.sleep(0.1)
    if not GPIO.input(17):
        print("SW2")
        # wait for button to be released
        while not GPIO.input(17):
            time.sleep(0.1)
    if not GPIO.input(18):
        print("SW4")
        # wait for button to be released
        while not GPIO.input(18):
            time.sleep(0.1)
    if not GPIO.input(27):
        print("SW3")
        # wait for button to be released
        while not GPIO.input(27):
            time.sleep(0.1)

# close GPIO access
GPIO.cleanup()
