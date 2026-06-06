import logging
import unittest
import re
import datetime

import time
from unittest.mock import MagicMock, patch

from cda.Sensor.SensorManager import SensorManager
from cda.Sensor.MoistureSensor import MoistureSensor
from cda.Sensor.LightSensor import LightSensor
from cda.Sensor.TempHumSensor import TempHumSensor

import  common.ConfigUtil as ConfigUtil

class SensorManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SensorManager class....")
        
        self.sMgr = SensorManager()
        #TODO: instantiate default data message listener
        pass 

    def setUp(self):
        pass 

    def tearDown(self):
        pass

    def testManagerStart(self):
        self.assertIsInstance(self.sMgr.m_sensor,MoistureSensor)
        self.assertIsInstance(self.sMgr.l_sensor,LightSensor)
        self.assertIsInstance(self.sMgr.th_sensor,TempHumSensor)
        
        self.sMgr.startManager()
        job_list = self.sMgr.scheduler.get_jobs()

        self.assertGreaterEqual(len(job_list),1)
        pass 

    def testExecuteRead(self):
        self.sMgr.execute_read(self.sMgr.m_sensor)
        self.sMgr.execute_read(self.sMgr.l_sensor)
        self.sMgr.execute_read(self.sMgr.th_sensor)
        data = self.sMgr.get_telemetry()
        logging.info(f"captured data: {data}")

        temp_hum_data, timestamp = data[self.sMgr.th_sensor.getName()]
        self.assertIsInstance(temp_hum_data, tuple)
        self.assertEqual(len(temp_hum_data), 2)
        self.assertIsNotNone(temp_hum_data[0])
        self.assertIsNotNone(temp_hum_data[1])
        self.assertIsNotNone(timestamp)
        

    def testDataCaching(self):
        self.sMgr.execute_read(self.sMgr.m_sensor)
        self.sMgr.execute_read(self.sMgr.l_sensor)
        self.sMgr.execute_read(self.sMgr.th_sensor)
        data = self.sMgr.data_cache
        #moisture sensor validation
        self.assertIsInstance(data['moisture_sensor'][0][0],int)
        self.assertIsInstance(data['moisture_sensor'][1],datetime.datetime)

        #light sensor validation
        self.assertIsInstance(data['light_sensor'][0][0],int)
        self.assertIsInstance(data['light_sensor'][0][1],float)
        self.assertIsInstance(data['light_sensor'][1],datetime.datetime)

        #temperature and humidity sensor validation
        self.assertIsInstance(data['temp_humidity_sensor'][0][0],float)
        self.assertIsInstance(data['temp_humidity_sensor'][0][1],float)
        self.assertIsInstance(data['temp_humidity_sensor'][1],datetime.datetime)
    def testGetTelemetry(self):
        pass

    def test_execute_read_handles_sensor_exception(self):
        """Test that execute_read logs error and skips cache update when sensor fails."""
        failing_sensor = MagicMock()
        failing_sensor.getName.return_value = 'failing_sensor'
        failing_sensor.getTelemetry.side_effect = RuntimeError('Sensor read failed')
        
        # Set a baseline value in cache
        self.sMgr.data_cache['failing_sensor'] = ('old_value', datetime.datetime(2020, 1, 1))
        
        # Call execute_read with the failing sensor
        self.sMgr.execute_read(failing_sensor)
        
        # Verify cache was NOT updated (old value remains)
        self.assertEqual(self.sMgr.data_cache['failing_sensor'][0], 'old_value')

    def test_start_manager_handles_scheduler_exception(self):
        """Test that startManager logs error but continues when scheduler fails to start."""
        # Mock the scheduler start to fail
        with patch.object(self.sMgr.scheduler, 'start', side_effect=RuntimeError('Scheduler failed')):
            # This should not raise an exception
            self.sMgr.startManager()
            
            # Verify jobs were still added (they're added before start() is called)
            jobs = self.sMgr.scheduler.get_jobs()
            self.assertEqual(len(jobs), 3)

    def testManagerStop(self):
        self.sMgr.stopManager()
        pass

    

    
