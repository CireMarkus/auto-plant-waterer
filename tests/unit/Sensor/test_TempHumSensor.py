import logging
import unittest
import time

from cda.Sensor.TempHumSensor import TempHumSensor

class TempHumSensorTest(unittest.TestCase):
    """
    Validate the functionality of the cpu utilization task. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing TempSensor class...")
        self.sensorName = 'TempSensor'
        self.sensorType = '1'
        self.sensor = TempHumSensor(self.sensorName,self.sensorType)
    
    def testGetName(self):
        self.assertEqual(self.sensor.getName(),self.sensorName)

    def testGetType(self):
        self.assertEqual(self.sensor.getTypeID(),self.sensorType)

    def testGetTelemetryValue(self):        
        for i in range(0,20):
            val = self.sensor.getTelemetry()
            self.assertIsInstance(val, tuple)
            self.assertEqual(len(val), 2)
            temperature = val[0]
            humidity = val[1]
            logging.info(f" temp: {temperature} C, humidity: {humidity}")
            self.assertIsNotNone(temperature)
            self.assertIsNotNone(humidity)
            time.sleep(1)
        