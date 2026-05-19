import logging

from cda.Sensor.BaseSensor import BaseSensor

import common.ConfigConst as ConfigConst
import common.ConfigUtil as ConfigUtil

_LIBS_AVAILABLE = True
try: 
    import board # pyright: ignore[reportMissingImports]
    import adafruit_ahtx0 # pyright: ignore[reportMissingImports] 
except: 
    _LIBS_AVAILABLE = False


class TempHumSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            name = ConfigUtil.TEMPHUM_SENSOR_NAME,
            typeID = ConfigConst.TEMPHUM_SENSOR_TYPE,
            floor = ConfigConst.TEMPHUM_SENSOR_FLOOR,
            ceiling = ConfigConst.TEMPHUM_SENSOR_CEILING)

        use_hw_cfg = ConfigUtil.use_hardware()
        if _LIBS_AVAILABLE and use_hw_cfg: 
            try: 
                self._sensor = adafruit_ahtx0.AHTx0(board.I2C())
            except Exception as e: 
                logging.error(f"The following error has occured during initialization: {e}.")
                exit()
        else:
            logging.info("Using simulated moisture sensor (config or missing libs)")
            #self._sensor = SimulatedTempHumSensor()
    
    def getTemp(self):
        #Temp is returned in Celcius
        return self._sensor.temperature
    
    def getHumidity(self):
        return self._sensor.relative_humidity
    
    def getTelemetry(self) -> tuple:
        return (self.getTemp(),self.getHumidity())