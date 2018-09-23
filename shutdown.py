#!/bin/python

import RPi.GPIO as GPIO
import time
import os

# Use the Broadcom SOC Pin numbers 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Shutdown and Reboot Functions 
def Shutdown(channel): 
	print "Shutting Down..."
	time.sleep(3)
	os.system("sudo shutdown -h now") 
def Reboot(channel):
        print "Rebooting..."
        time.sleep(3)
        os.system("sudo reboot -n")

# Add our function to execute when the button pressed event happens 
GPIO.add_event_detect(21, GPIO.FALLING, callback = Shutdown, bouncetime = 2000) 
GPIO.add_event_detect(20, GPIO.RISING, callback = Reboot, bouncetime = 2000)


# Now wait! 
while 1: 
	time.sleep(1)
