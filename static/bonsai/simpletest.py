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


# Completely Wet ~ 10700
# Completely Dry ~ 14350

completelyWet = 10700
completelyDry = 14350

while True:
    values = [0]*4
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)
    
    currentMoisture = '{0:>6}'.format(*values)
    
    if currentMoisture < completelyWet:
        currentMoisture = completelyWet
    elif currentMoisture > completelyDry:
        currentMoisture = completelyDry

    print("Current Moisture: " + currentMoisture)

    

    time.sleep(2)
