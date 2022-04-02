from measure_temp import readTemp
import time
import math
import RGB1602
import os
import RPi.GPIO as GPIO
import smtplib


# Initialise
running = False

led = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

colorR = 64
colorG = 128
colorB = 64
lcd=RGB1602.RGB1602(16,2)

smtp_username = "enter_username_here"
smtp_password = "enter_password_here"
smtp_host = "enter_host_here"
smtp_port = 25

smtp_sender = "sender@email.com"
smtp_receivers = ['receiver@email.com']

message_dead = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Warning, no moisture detected! Plant death imminent!!! :'(
"""

message_alive = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Panic over! Plant has water again :)
"""

def sendEmail(smtp_message):
	try:
		smtpObj = smtplib.SMTP(smtp_host, smtp_port)
		smtpObj.login(smtp_username, smtp_password) # If you don't need to login to your smtp provider, simply remove this line
		smtpObj.sendmail(smtp_sender, smtp_receivers, smtp_message)         
		print("Successfully sent email")
	except smtplib.SMTPException:
		print("Error: unable to send email")

def callback(channel):  
	if GPIO.input(channel):
		print("LED off")
		sendEmail(message_dead)
	else:
		print("LED on")
		sendEmail(message_alive)

GPIO.setmode(GPIO.BCM)

channel = 17
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)



if __name__ == "__main__":
    
    running = True
    while running:
        os.system("clear")        
        try:
            
                
            get_temp = readTemp()
            print(get_temp)
            lcd.setRGB(colorR,colorG,colorB);
            lcd.setCursor(0, 0)
            lcd.printout(get_temp)
            lcd.setCursor(0, 1)
            
            if GPIO.input(channel):
                soil = "Moisture: Water "
                print("Alert: On")
                GPIO.output(led, GPIO.HIGH)
            else:
                soil = "Moisture: Good  "
                print("Alert: Off")
                GPIO.output(led, GPIO.LOW)
            print(soil)
            lcd.printout(soil)
        
            time.sleep(10)
            
        except TypeError as error:
            print(error)
            continue
