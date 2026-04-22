import board
import adafruit_veml7700
import logging

import BaseSensor
import common.ConfigConst as ConfigConst

class LightSensor(BaseSensor):
    
    def __init__(self):
        super(LightSensor,self).__init__(\
            name = ConfigConst.LIGHT_SENSOR_NAME,\
            typeID = ConfigConst.LIGHT_SENSOR_TYPE,\
            floor = ConfigConst.LIGHT_SENSOR_FLOOR,\
            ceiling = ConfigConst.LIGHT_SENSOR_CEILING)
        
        try: 
            self._sensor = adafruit_veml7700.VEML7700(board.I2C())
        except Exception as e:
            logging.error(f"The following error has occured during initialization: {e}")
        self.__ITARRAY =[self._sensor.ALS_25MS,self._sensor.ALS_50MS,self._sensor.ALS_100MS,self._sensor.ALS_200MS,self._sensor.ALS_400MS,self._sensor.ALS_800MS]
        self.__GAINARRAY = [self._sensor.ALS_GAIN_1_8,self._sensor.ALS_GAIN_1_4,self._sensor.ALS_GAIN_1,self._sensor.ALS_GAIN_2]
        self.__gainIndex = 0
        self.__itIndex = 0
        self._sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
        self._sensor.light_gain = self.__GAINARRAY[self.__gainIndex]

    def _autoAdjust(self):
        if(self._sensor.light < 100):
            if(self.__itIndex < len(self.__ITARRAY)-1):
                self.__itIndex += 1
                self._sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                return
            elif(self.__gainIndex < len(self.__GAINARRAY)-1):
                self.__gainIndex += 1
                self.__itIndex = 0
                self._sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                self._sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
                return
        elif (self._sensor.light > 10000):
            if(self.__itIndex > 0):
                self.__itIndex -= 1
                self._sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                return
            elif(self.__gainIndex > 0):
                self.__gainIndex -= 1
                self.__itIndex = len(self.__ITARRAY)-1
                self._sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
                self._sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
                return
        return
    
    def getTelemetry(self) -> tuple:
        self._autoAdjust()
        return (self._sensor.light,self._sensor.lux)
    
    def __str__(self):
        print(f"Current light value: {self._sensor.light} \
            Current lux value: {self._sensor.lux}")