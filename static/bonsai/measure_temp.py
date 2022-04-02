import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D26)

def readTemp():
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9/5) + 32
        humidity = dhtDevice.humidity
        return "{:.1f} F / {}% ".format(temperature_f, humidity)
        
    except RuntimeError as error:
        pass
    except Exception as error:
        pass
