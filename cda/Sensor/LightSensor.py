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
        raw_light = self.__sensor.light
        if 500 <= raw_light <= 8000:
            return # Already in a stable linear range

        # 1. Calculate what the sensitivity SHOULD be to hit a target of 5000
        current_sensitivity = self.__GAINARRAY[self.__gainIndex] * self.__ITARRAY[self.__itIndex]
        target_sensitivity = (5000 / raw_light) * current_sensitivity

        # 2. Find the best Gain/IT combination to hit that target_sensitivity
        # Start with the lowest gain and increase IT linearly
        best_gain_idx = 0
        best_it_idx = 0
        min_diff = float('inf')

        for g_idx, g_val in enumerate(self.__GAINARRAY):
            for it_idx, it_val in enumerate(self.__ITARRAY):
                test_sensitivity = g_val * it_val
                diff = abs(test_sensitivity - target_sensitivity)
                
                if diff < min_diff:
                    min_diff = diff
                    best_gain_idx = g_idx
                    best_it_idx = it_idx

        # 3. Apply the settings
        self.__gainIndex = best_gain_idx
        self.__itIndex = best_it_idx
        self.__sensor.light_gain = self.__GAINARRAY[self.__gainIndex]
        self.__sensor.light_integration_time = self.__ITARRAY[self.__itIndex]
        
    def getTelemetry(self) -> tuple:
        self._autoAdjust()
        return (self._sensor.light,self._sensor.lux)
    
    def __str__(self):
        print(f"Current light value: {self._sensor.light} \
            Current lux value: {self._sensor.lux}")
        
if __name__ == "__main__":
    light = LightSensor()
    while (True):
        print(light)