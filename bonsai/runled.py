import RPi.GPIO as GPIO
import time

led = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
print("led on")
GPIO.output(led, GPIO.HIGH)
time.sleep(1)
print("led off")
GPIO.output(led, GPIO.LOW)