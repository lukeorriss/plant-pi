from flask import Flask, request, jsonify
from datetime import datetime
import mysql.connector

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Plant Pi Monitoring
from measure_temp import readTemp
import time
import math
import RGB1602
import os
import RPi.GPIO as GPIO
import smtplib
import ssl
from email.mime.text import MIMEText

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

    msg = MIMEText(body)
    msg['From'] = "No Reply | Plant Update"
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    s.sendmail(sender, recipients, msg.as_string())
    s.close()

def readSensors():
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

        with open("logs/monitoring/log.txt", "a") as f:
            f.write(strToWrite)

        return strHumiture
    except TypeError as error:
        print(error)
        with open("logs/errors/log.txt", "a") as e:
            strToErrorWrite = "{date:%s, time: %s, error: %s},\n" % (currentDate, currentTime, error)
            e.write(strToErrorWrite)
        




@app.route('/')
def plant():
    return app.send_static_file('index.html')

@app.route('/api/plantpi/get_update',methods=['GET','POST'])
def get_plant_update():
    if request.method != "POST":
        return "no data"
    today = datetime.now()
    d1 = today.strftime("%d/%m/%Y")
    t1 = today.strftime("%H:%M:%S")


    ldata = {"result":"success", "date": [d1], "time": [t1], "hum":humidity, "temp":temperature}
    return jsonify(data=ldata)

@app.route('/api/plantpi/checksystem', methods=['GET','POST'])
def check_system():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/checkserver', methods=['GET','POST'])
def check_server():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/testservices', methods=['GET','POST'])
def test_services():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/testsensors', methods=['GET','POST'])
def test_sensors():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/restartserver', methods=['GET','POST'])
def restart_server():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/restartplantpi', methods=['GET','POST'])
def restart_plantpi():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/shutdownserver', methods=['GET','POST'])
def shutdown_server():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/shutdownplantpi', methods=['GET','POST'])
def shutdown_plantpi():
    if request.method != "POST":
        return False
    ldata = {"result":"success"}
    return jsonify(data=ldata)

@app.route('/api/plantpi/toggle_api', methods=['GET','POST'])
def toggle_api_settings():
    if request.method != "POST":
        return False
    
    if request.form["log_api"]:
        print("logapi")

    with open("./settings.json", "a") as f:
        f.write("\n")
    ldata = {"result":"success"}
    return jsonify(data=ldata)






if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
