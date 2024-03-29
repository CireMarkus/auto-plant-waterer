import time
import board
import adafruit_dht

class TempHumSensor: 
    __dht = adafruit_dht.DHT22(board.D26)
    
    def __init__(self):
        pass
    
    
    def getTempFarenheit(self):
        time.sleep(2.5)
        return self.__dht.temp *(9.0/5.0) + 32.0
    
    def getHumidity(self):
        time.sleep(2.5)
        return self.__dht.humidity
    
        