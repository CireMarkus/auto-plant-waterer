import logging
import unittest

from cda.system.SystemUtilTasks import SystemDiskUtilTask

class SystemCpuUtilTaskTest(unittest.TestCase):
    """
    Validate the functionality of the disk utilization task. 
    """
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemDiskUtilTask class...")
        self.diskUtilTask = SystemDiskUtilTask()
    
    def testGetTelemetryValue(self):
        val = self.diskUtilTask.getTelemetryValue()
        
        self.assertGreaterEqual(val, 0.0)
        logging.info("Disk utilization: %s%", str(val))
        