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



def getMessageDead(reason, temperature, humidity, moisture):
    return """
Hello, there is an issue with your Bonsai.

Needs Attention: """ + reason + """

Temperature: """ + temperature + """
Humidity: """ + humidity + """
""" + moisture + """
"""

def getMessageAlive(temperature, humidity, moisture):
    return """
Hello, there is an update with your Bonsai.

Everything looks to be good. 
Temperature: """ + temperature + """
Humidity: """ + humidity + """
""" + moisture + """
"""

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

def callback(channel):  
	if GPIO.input(channel):
		print("LED off")
		#sendEmail("dead", "Issue with Bonsai")
	else:
		print("LED on")
		sendEmail("alive", "Resolved Issue with Bonsai")

GPIO.setmode(GPIO.BCM)

channel = 17
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)



if __name__ == "__main__":
    running = True
    time_elapsed = 0
    while running:
        
        #os.system("clear")        
        
        try:
            get_temp = readTemp()
            #print(get_temp)
            try:
                return_temp = get_temp.split(" / ")
                ltemp = return_temp[0]
                lhumidity = return_temp[1]
                local_temp = ltemp.split(" ")
                local_humidity = lhumidity.split("%")
                
            except AttributeError as error:
                print("Couldn't determine split. Continuing...")
                e = open("logs/errors/log.txt", "a")
                strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
                e.write(strToErrorWrite)
                e.close()
                continue
            
            temperature = f"{local_temp[0]}"
            humidity = f"{local_humidity[0]}"
            strHumiture = temperature + " / " + humidity
            time_elapsed = time_elapsed + 1
            date = datetime.now()
            currentDate = date.strftime("%d/%m/%Y")
            currentTime = date.strftime("%H:%M:%S")
            
            
            lcd.setRGB(255,0,0);
            lcd.setCursor(0, 0)
            lcd.printout(strHumiture)
            lcd.setCursor(0, 1)
            alert = 0
            monitorSoil = 0
            
            if GPIO.input(channel):
                soil = "Moisture: Water "
                print("Alert: On")
                alert = 1
                monitorSoil = 1
                #alert()
                GPIO.output(led, GPIO.HIGH)
            else:
                soil = "Moisture: Good  "
                print("Alert: Off")
                alert = 0
                monitorSoil = 0
                GPIO.output(led, GPIO.LOW)
            print(soil)
            lcd.printout(soil)

            
            if time_elapsed == 180:
                time_elapsed = 0
                print("Sending Update Email")
                sendEmail("alive", "Check In: All Good", "", ltemp, lhumidity, soil)
            print(f"Time Elapsed: {time_elapsed}/180")
            time.sleep(10)
            
            strToWrite = "{date:%s, time:%s, temp:%s, hum:%s, stamp: %s, alert: %s, soil: %s},\n" % (currentDate, currentTime, temperature, humidity, time_elapsed, alert, monitorSoil)

            print(strToWrite)
            
            f = open("logs/monitoring/log.txt", "a")
            f.write(strToWrite)
            f.close()
            
            
            
            
        except TypeError as error:
            print(error)
            e = open("logs/errors/log.txt", "a")
            strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
            e.write(strToErrorWrite)
            e.close()
            continue
