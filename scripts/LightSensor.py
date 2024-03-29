import board
import adafruit_veml7700

class LightSensor: 
    
    __i2c = None
    __sensor = None
    __gainIndex = None
    __itIndex = None
    
    def __init__(self) -> None:
        try:
            self.__i2c = board.I2C() #uses board.SCL and board.SDA
            self.__sensor = adafruit_veml7700.VEML7700(self.__i2c)
        except Exception as e: 
            print("The following error has occured during initialization: {}".format(e))
            exit(1)
        self.__ITARRAY =[self.__sensor.ALS_25MS,self.__sensor.ALS_50MS,self.__sensor.ALS_100MS,self.__sensor.ALS_200MS,self.__sensor.ALS_400MS,self.__sensor.ALS_800MS]
        self.__GAINARRAY = [self.__sensor.ALS_GAIN_1_8,self.__sensor.ALS_GAIN_1_4,self.__sensor.ALS_GAIN_1,self.__sensor.ALS_GAIN_2]
        self.__gainIndex = 0
        self.__itIndex = 0
        self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
        self.__sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
    
    #function that will automatically adjust the sensitivity of the sensor as the amibient light changes.
    def __autoAdjust(self):
        if(self.__sensor.light < 100):
            if(self.__itIndex < len(self.__ITARRAY)-1):
                self.__itIndex += 1
                self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                return
            elif(self.__gainIndex < len(self.__GAINARRAY)-1):
                self.__gainIndex += 1
                self.__itIndex = 0
                self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                self.__sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
                return
        elif (self.__sensor.light > 10000):
            if(self.__itIndex > 0):
                self.__itIndex -= 1
                self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                return
            elif(self.__gainIndex > 0):
                self.__gainIndex -= 1
                self.__itIndex = len(self.__ITARRAY)-1
                self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                self.__sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
                return
        return
    
    #returns the current light intensity with lux first and voltage second
    def getCurrentLight(self):
        self.__autoAdjust()
        return (self.__sensor.lux,self.__sensor.light)
    def getIntegrationTime(self):
        return self.__sensor.integration_time_value()
    def getGain(self):
        return self.__sensor.gain_value()
    
    
if __name__ == "__main__":
    light = LightSensor()
    while(True):
        vals = light.getCurrentLight()
        print("Current Lux value: {:6.0f} Current light value: {:6d} Gain: {:.3f} Integration time: {:3d}".format(vals[0],vals[1],light.getGain(),light.getIntegrationTime()), end='\r')