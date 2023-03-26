import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D26)

while True:
    temp = dht.temperature * (9/5) +32
    hum = dht.humidity
    
    print("temperature: {}, humidity: {}".format(temp,hum))
