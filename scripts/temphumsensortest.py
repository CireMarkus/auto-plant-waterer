import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.20)

while True:
    temp, hum = dht.measure()
    
    print("temperature: {}, humidity: {}".format(temp,hum))