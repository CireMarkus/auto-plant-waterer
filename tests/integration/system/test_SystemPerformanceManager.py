import logging 
import unittest 

from time import sleep

from cda.system.SystemPerformanceManager import SystemPeformanceManager
#TODO: import the default data message listener

class SystemPerformanceManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SystemPerformanceManager class...")
        self.spMgr = SystemPeformanceManager()
        #TODO: instantiate default data message listener
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testHandleTelemetry(self):
        self.spMgr.handleTelemetry()
        
    def testStartAndStopManager(self):
        self.spMgr.startManager()
        sleep(10)
        self.spMgr.stopManager()
    
    
        
