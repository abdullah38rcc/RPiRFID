#!/usr/bin/python

import RPi.GPIO as GPIO
import time

RED = 23
GREEN = 7
BLUE = 22

def initGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RED, GPIO.OUT) # Pin 23, GPIO11, SCLK
    GPIO.setup(GREEN, GPIO.OUT) # Pin 22, GPIO25, ARM_TCK
    GPIO.setup(BLUE, GPIO.OUT) # Pin 7, GPIO4, GPCLK0

"""
If no badge present, turn blue light on.
If badge matches turn green light on.
If badge doesn't match turn on red light.
"""

def noBadge():
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.HIGH)

def badgeMatch():
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(BLUE, GPIO.LOW)

def badgeNotFound():
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)

def testSeq():
    GPIO.output(RED, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(BLUE, GPIO.LOW)
    time.sleep(.5)
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(BLUE, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)
    time.sleep(.5)

def allLampsOn():
    # while True:
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(BLUE, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)

if __name__ == "__main__":
    testSeq()
    allLampsOn()
