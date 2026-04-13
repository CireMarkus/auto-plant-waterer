import logging
import unittest

from cda.system.SystemUtilTasks import SystemNetOutUtilTask

class SystemNetOutUtilTaskTest(unittest.TestCase):
    """
    Validate the functionality of the Network sent utilization task. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemNetOutUtilTask class...")
        self.NetOutUtilTask = SystemNetOutUtilTask()
    
    def testGetTelemetryValue(self):
        val = self.NetOutUtilTask.getTelemetryValue()
        
        self.assertGreaterEqual(val, 0.0)
        logging.info(f"Net Out utilization: {val} bytes.")
        