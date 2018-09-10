import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 2
GPIO_ECHO = 3

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger High
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.1ms low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    startTime = time.time()
    endTime = time.time()
 
    # store start time
    while GPIO.input(GPIO_ECHO) == 0:
        startTime = time.time()
 
    # store arrival
    while GPIO.input(GPIO_ECHO) == 1:
        endTime = time.time()
 
    # elapsed time
    TimeElapsed = endTime - startTime
    # multiply with speed of sound (34300 cm/s)
    # and division by two
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 

while True:
    dist = distance()
    print ("Entfernung = %.1f cm" % dist)
    time.sleep(0.5)
 

