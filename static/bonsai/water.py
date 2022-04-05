import time
import math
import os
import RPi.GPIO as GPIO
from datetime import datetime

moisture = 22
pump = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(moisture, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)



# while True: 
#     GPIO.output(pump, GPIO.HIGH)
#     time.sleep(5)
#     GPIO.output(pump, GPIO.LOW)
#     time.sleep(5)

while True:
    if GPIO.input(moisture):
        print("no water")
        time.sleep(2)
    else:
        print("water")
        time.sleep(2)