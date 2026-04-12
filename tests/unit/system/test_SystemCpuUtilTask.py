import logging
import unittest

from cda.system.SystemUtilTasks import SystemCpuUtilTask

class SystemCpuUtilTaskTest(unittest.TestCase):
    """
    Validate the functionality of the cpu utilization task. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemCpuUtilTask class...")
        self.cpuUtilTask = SystemCpuUtilTask()
    
    def testGetTelemetryValue(self):
        val = self.cpuUtilTask.getTelemetryValue()
        
        self.assertGreaterEqual(val, 0.0)
        logging.info("CPU utilization: %s%", str(val))
        