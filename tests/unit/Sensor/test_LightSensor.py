import logging
import unittest
import time

from cda.Sensor.LightSensor import LightSensor

class LightSensorTest(unittest.TestCase):
    """
    Validate the functionality of the LightSensor. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing LightSensor class...")
        self.sensorName = 'LightSensor'
        self.sensorType = '1'
        self.sensor = LightSensor(self.sensorName,self.sensorType)

    def testGetTelemetryValue(self):        
        for i in range(0,20):
            val = self.sensor.getTelemetry()
            light = val[0]
            lux = val[1]
            logging.info(f" light: {light}, lux: {lux}")
            self.assertIsNotNone(light)
            self.assertIsNotNone(lux)
            time.sleep(.10)
        