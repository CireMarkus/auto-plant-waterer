import time
import board
import adafruit_ahtx0

class TempHumSensor: 
    _sensor = adafruit_ahtx0.AHTx0(board.I2C())
    
    def __init__(self):
        pass
    
    
    def getTempFarenheit(self):
        return self._sensor.temperature *(9.0/5.0) + 32.0
    
    def getHumidity(self):
        return self._sensor.relative_humidity
    
        