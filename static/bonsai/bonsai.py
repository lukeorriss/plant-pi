from measure_temp import readTemp
import time
import math
import RGB1602
import os
import RPi.GPIO as GPIO
from datetime import datetime
import Adafruit_ADS1x15

# Initialise
running = False

# Initialise LED
led = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

# Initialise Moisture Sensor
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
pump = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pump, GPIO.OUT)
completelyWet = 10700
completelyDry = 14350

# Initialise Screen
colorR = 64
colorG = 128
colorB = 64
lcd = RGB1602.RGB1602(16,2)


if __name__ == "__main__":
    running = True
    time_elapsed = 0
    while running:
        try:
            # Get Current Date and Time
            date = datetime.now()
            currentDate = date.strftime("%d/%m/%Y")
            currentTime = date.strftime("%H:%M:%S")
            getHumiture = readTemp()

            # Try to read Temperature and Humidity
            try:
                returnHumiture = getHumiture.split(" / ")
                ltemp = returnHumiture[0]
                lhumidity = returnHumiture[1]
                local_temp = ltemp.split(" ")
                local_humidity = lhumidity.split("%")
            except AttributeError as error:
                print("Couldn't determine split. Continuing...")
                print(error)
                with open("logs/errors/log.txt", "a") as e:
                    strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
                    e.write(strToErrorWrite)
                time.sleep(2)
                continue
            
            # Temperature and Humidity Formatting
            temperature = f"{local_temp[0]} F"
            humidity = f"{local_humidity[0]} %"
            strHumiture = f'{temperature} / {humidity}'
            time_elapsed = time_elapsed + 1
            
            
            # Moisture Level Sensor Formatting
            values = [0]*4
            for i in range(4):
                values[i] = adc.read_adc(i, gain=GAIN)
            currentMoisture = int('{0:>6}'.format(*values))
            
            if currentMoisture < completelyWet:
                currentMoisture = completelyWet
            elif currentMoisture > completelyDry:
                currentMoisture = completelyDry

            moistureMinus = currentMoisture - 10700
            inversePercentage = round((moistureMinus / 3650) * 100, 2)
            moisturePercentage = round(100 - inversePercentage, 2)
            
            # Check if Soil Moisture is low, if it is: turn on the pump. If not, turn it off
            watering = False
            if moisturePercentage < 10:
                GPIO.output(pump, GPIO.HIGH)
                watering = True
            if watering and moisturePercentage < 80:
                GPIO.output(pump, GPIO.HIGH)
            else: 
                GPIO.output(pump, GPIO.LOW)
                watering = False


            # Constant Checks, alerts if Temp/ Humidity too high/low
            if (
                float(local_temp[0]) > 90
                or float(local_temp[0]) < 40
                or float(local_humidity[0]) > 90
                or float(local_humidity[0]) < 30
                or moisturePercentage < 10
            ):
                lcd.setRGB(255, 0, 0)
            else:
                lcd.setRGB(0,0,168);


            # Write Stats to screen
            lcd.setCursor(0, 0)
            lcd.printout(strHumiture)
            lcd.setCursor(0, 1)
            lcd.printout("Soil: " + str(moisturePercentage) + "%         ")


            time.sleep(3)

            # Terminal Logging
            strToWrite = "{date:%s, time:%s, temp:%s, hum:%s, stamp: %s}?" % (currentDate, currentTime, temperature, humidity, time_elapsed)

            print(strHumiture)
            print("Current Moisture: " + str(moisturePercentage) + "% Wet")
            #print(f"Running For: {time_elapsed * 10} seconds")
            print("Output: " + strToWrite)



            # Log Output to file
            
            with open("logs/monitoring/log.txt", "a") as f:
                f.write(strToWrite)
        except TypeError as error:
            print(error)
            with open("logs/errors/log.txt", "a") as e:
                strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
                e.write(strToErrorWrite)
            continue
