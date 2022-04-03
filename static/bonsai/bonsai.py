from measure_temp import readTemp
import time
import math
import RGB1602
import os
import RPi.GPIO as GPIO
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime


# Initialise
running = False

# Initialise LED
led = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

# Initialise Screen
colorR = 64
colorG = 128
colorB = 64
lcd = RGB1602.RGB1602(16,2)

# Initialise Email
smtp_server = "smtp.titan.email"
smtp_port = 465
sender = "noreply@lukeorriss.com"
password = "6#73K7HRfT&hDED!"
recipients = ['stuff@lukeorriss.com', 'lukeorriss@outlook.com']

def sendEmail(alert_type, subject, reason, temperature, humidity, moisture):
    context = ssl.create_default_context()
    s = smtplib.SMTP_SSL(smtp_server, smtp_port, context)
    s.set_debuglevel(0)
    s.ehlo()
    s.login(sender, password)

    if alert_type == "dead":
        body = getMessageDead(reason, temperature, humidity, moisture)
    else:
        body = getMessageAlive(temperature, humidity, moisture)

    msg = MIMEText(body)
    msg['From'] = "No Reply | Plant Update"
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    s.sendmail(sender, recipients, msg.as_string())
    s.close()


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

            temperature = f"{local_temp[0]} F"
            humidity = f"{local_humidity[0]} %"
            strHumiture = f'{temperature} / {humidity}'
            time_elapsed = time_elapsed + 1

            # Constant Checks, alerts if Temp/ Humidity too high/low
            if (
                float(local_temp[0]) > 90
                or float(local_temp[0]) < 40
                or float(local_humidity[0]) > 90
                or float(local_humidity[0]) < 30
            ):
                lcd.setRGB(255, 0, 0)
                GPIO.output(led,GPIO.HIGH)
            else:
                lcd.setRGB(0,100,255);
                GPIO.output(led,GPIO.LOW)

            # Write Stats to screen
            lcd.setCursor(0, 0)
            lcd.printout(strHumiture)
            lcd.setCursor(0, 1)
            alert = 0
            monitorSoil = 0




            print(f"Time Elapsed: {time_elapsed}/180")
            time.sleep(10)

            strToWrite = "{date:%s, time:%s, temp:%s, hum:%s, stamp: %s, alert: %s},\n" % (currentDate, currentTime, temperature, humidity, time_elapsed, alert)

            print(strToWrite)

            with open("logs/monitoring/log.txt", "a") as f:
                f.write(strToWrite)
        except TypeError as error:
            print(error)
            with open("logs/errors/log.txt", "a") as e:
                strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
                e.write(strToErrorWrite)
            continue
