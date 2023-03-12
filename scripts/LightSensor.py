import board
import adafruit_veml7700

class LightSensor: 
    
    __i2c = None
    __veml7700 = None
    __gain = None
    __iTime = None
    
    def __init__(self) -> None:
        try:
            self.__i2c = board.I2C() #uses board.SCL and board.SDA
            self.__veml7700 = adafruit_veml7700.VEML7700(self.__i2c)
            self.__gain = self.__veml7700.ALS_GAIN_1_8
            self.__iTime = self.__veml7700.ALS_25MS
            self.__veml7700.light_integration_time =self.__iTime
            self.__veml7700.light_gain = self.__gain
        except Exception as e: 
            print("The following error has occured during initialization: {}".format(e))
    
    #returns the current light intensity with lux first and voltage second
    def getCurrentLight(self):
        return (self.__veml7700.lux,self.__veml7700.light)
    

if __name__ == "__main__":
    light = LightSensor()
    while(True):
        vals = light.getCurrentLight()
        print("Current Lux value: {:0.3f} Current light value: {:6d}".format(vals[0],vals[1]), end='\r')