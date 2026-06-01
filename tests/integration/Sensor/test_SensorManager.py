import logging
import unittest

from time import sleep 

from cda.Sensor.SensorManager import SensorManager

class SensorPerformanceManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SensorManager class....")
        
        sMgr = SensorManager()
        #TODO: instantiate default data message listener
        pass 

    def setUp(self):
        pass 

    def tearDown(self):
        pass

    def testManagerStart(self):
        pass 

    def testExecuteRead(self):
        pass

    def testDataCaching(self):
        pass

    def testGetTelemetry(self):
        pass

    def testManagerStop(self):
        pass

    

    
