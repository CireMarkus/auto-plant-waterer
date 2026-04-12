import logging
import unittest

from cda.system.SystemUtilTasks import SystemMemUtilTask


class SystemMemUtilTaskTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemMemUtilTask class...")
        self.memUtilTask = SystemMemUtilTask()
        
    def testGetTelemetryValue(self):
        val = self.memUtilTask.getTelemetryValue()
        
        self.assertGreaterEqual(val,0.0)
        logging.info("CPU utilization: %s%",str(val))\
            