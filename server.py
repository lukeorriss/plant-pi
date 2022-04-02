from flask import Flask, request, jsonify
from datetime import datetime
import mysql.connector

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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

    temp = 65.45
    hum = 59.60

    def get_temp():
        return temp
    def get_hum():
        return hum

    temp = temp + 2
    hum = hum + 2

    get_temperature = get_temp()
    get_humidity = get_hum()

    ldata = {"result":"success", "date": [d1], "time": [t1], "hum":str(get_humidity), "temp":str(get_temperature)}
    f = open("./api_logs/log.txt", "a")
    f.write("{Date:" + d1 + ", Time:" + t1 + ", Call:" + str(request) + "}\n")
    f.close()
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








if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
