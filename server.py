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

    file1 = open('/var/www/plant-pi/static/bonsai/logs/monitoring/log.txt', 'r')
    Lines = file1.readlines()
    count = 0
    

    ldata = {"result":"success", "date": [d1], "time": [t1], "data":[Lines]}
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
