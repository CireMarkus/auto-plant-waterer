import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D26)

while True:
    try:
        temp = dht.temperature * (9/5) +32
        hum = dht.humidity
        print("Temperature(F): {}, Humidity: {}".format(temp,hum))
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])
    
    
    
    