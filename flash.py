import RPi.GPIO as GPIO
import time

RED = 23
GREEN = 22
BLUE = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED, GPIO.OUT) # Pin 23, GPIO11, SCLK
GPIO.setup(GREEN, GPIO.OUT) # Pin 22, GPIO25, ARM_TCK
GPIO.setup(BLUE, GPIO.OUT) # Pin 7, GPIO4, GPCLK0

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
	while True:
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.HIGH)

if __name__ == "__main__":
	testSeq()
	allLampsOn()
