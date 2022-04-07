
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1


moisture = 22
pump = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(moisture, GPIO.IN)
GPIO.setup(pump, GPIO.OUT)

print('Reading ADS1x15 values, press Ctrl-C to quit...')

print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

while True:
    values = [0]*4
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    time.sleep(2)
