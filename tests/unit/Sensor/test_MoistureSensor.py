import logging
import unittest

from cda.Sensor.MoistureSensor import MoistureSensor

class SystemCpuUtilTaskTest(unittest.TestCase):
    """
    Validate the functionality of the cpu utilization task. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemCpuUtilTask class...")
        self.sensor = MoistureSensor("PM1MS","1")
    
    def testGetTelemetryValue(self):
        val = self.sensor.getTelemetry()
        
        
        logging.info(f"sensor value: {val}%")
        