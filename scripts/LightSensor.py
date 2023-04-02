import board
import adafruit_veml7700

class LightSensor: 
    
    __i2c = None
    __sensor = None
    __gain = None
    __iTime = None
    
    def __init__(self) -> None:
        try:
            self.__i2c = board.I2C() #uses board.SCL and board.SDA
            self.__sensor = adafruit_veml7700.VEML7700(self.__i2c)
            self.__gain = self.__sensor.ALS_GAIN_1_8 #gain of the sensor
            self.__iTime = self.__sensor.ALS_25MS #integration time
            self.__sensor.light_integration_time =self.__iTime
            self.__sensor.light_gain = self.__gain
        except Exception as e: 
            print("The following error has occured during initialization: {}".format(e))
    
    #returns the current light intensity with lux first and voltage second
    def getCurrentLight(self):
        return (self.__sensor.lux,self.__sensor.light)
    
    #TODO write function that will automatically adjust the sensitivity of the sensor as the amibient light changes.
    def autoAdjust(self):
        pass
    

if __name__ == "__main__":
    light = LightSensor()
    while(True):
        vals = light.getCurrentLight()
        print("Current Lux value: {:6.0f} Current light value: {:6d}".format(vals[0],vals[1]), end='\r')