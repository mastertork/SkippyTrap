#!/bin/python

import RPi.GPIO as GPIO
import time
import os

# Use the Broadcom SOC Pin numbers
GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Shutdown Button
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Reboot Button

GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Arm Trap Button
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Input from Sensor

GPIO.setup(18, GPIO.OUT) # Relay 1
GPIO.setup(23, GPIO.OUT) # Relay 2
GPIO.setup(24, GPIO.OUT) # Relay 3
GPIO.setup(25, GPIO.OUT) # Relay 4

# Set all Relays to HIGH
GPIO.output(18, 1)
GPIO.output(23, 1)
GPIO.output(24, 1)
GPIO.output(25, 1)

# Callbacks for Shutdown and Reboot Buttons
def Shutdown(channel):
        print "Shutting Down..."
        time.sleep(3)
        os.system("sudo shutdown -h now")

def Reboot(channel):
        print "Rebooting..."
        time.sleep(3)
        os.system("sudo reboot -n")

# Callbacks for the Trap Arm/Disarm/Trigger
def Arm(channel):
	if GPIO.input(channel):
		print "Arming Skippy Trap..."
		GPIO.add_event_detect(19, GPIO.FALLING, callback = Trigger, bouncetime = 2000)
		time.sleep(0.5)
	else:
		print "Locking Skippy Trap Open..."
		GPIO.remove_event_detect(19)
		time.sleep(0.5)

def Trigger(channel):
	GPIO.output(18, 0)
	print "Skippy Trap Triggered!!"
	time.sleep(3)
	GPIO.output(18, 1)
        time.sleep(0.5)

# Function to look for Shutdown or Reboot Buttons to be pressed
GPIO.add_event_detect(21, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)
GPIO.add_event_detect(20, GPIO.RISING, callback = Reboot, bouncetime = 2000)

# Function to look for "Arm Trap" button to be on or off
GPIO.add_event_detect(26, GPIO.BOTH, callback = Arm, bouncetime = 2000)

# Script Loop
try:
	print "Skippy Trap is Booted Up"
	while 1:
		time.sleep(1)
except KeyboardInterrupt:
	print "\n", "Skippy Trap Exiting..."
	GPIO.cleanup()

