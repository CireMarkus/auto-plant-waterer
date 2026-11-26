import colorsys
import logging
import time
import unittest
from unittest.mock import patch

from common.SampleProvider import SampleProvider
from cda.Sensor.SensorManager import SensorManager
from cda.Actuator.LED import LED

import common.ConfigUtil as ConfigUtil

class LedIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing SensorManager -> LED integration......")

    def setUp(self):
        min_val = ConfigUtil.sensor_parser("moisture_sensor","min_val")
        max_val = ConfigUtil.sensor_parser("moisture_sensor","max_val")
        self.led = LED(min_val,max_val)
        self.sensor_manager = SensorManager()
        pass 

    def test_moisture_data(self):
        # assert the sample provider is reading the CSV fixture
        sample_provider = SampleProvider('moisture_sensor')
        expected_value = int(sample_provider.next())

        # execute read of m_sensor to get new data
        self.sensor_manager.execute_read(self.sensor_manager.m_sensor)
        test_data = self.sensor_manager.get_telemetry()

        self.assertIn('moisture_sensor', test_data)
        self.assertIsInstance(test_data['moisture_sensor'], tuple)
        self.assertEqual(len(test_data['moisture_sensor']), 2)

        sensor_value, timestamp = test_data['moisture_sensor']
        self.assertIsInstance(sensor_value, tuple)
        self.assertGreaterEqual(len(sensor_value), 1)
        self.assertIsInstance(sensor_value[0], (int, float))
        self.assertIsNotNone(timestamp)

        new_led_val = sensor_value[0]
        self.assertEqual(new_led_val, expected_value)
        self.assertGreaterEqual(new_led_val, ConfigUtil.sensor_parser('moisture_sensor', 'min_val'))
        self.assertLessEqual(new_led_val, ConfigUtil.sensor_parser('moisture_sensor', 'max_val'))

        # update the LED color based on the sensor data
        self.led.updateLedColor(new_led_val)
        self.assertIsInstance(self.led.led.color, tuple)
        self.assertEqual(len(self.led.led.color), 3)
        self.assertTrue(all(isinstance(c, (int, float)) for c in self.led.led.color))

    def test_scheduler_updates_sensor_data(self):
        with patch.object(ConfigUtil, 'get_poll_rate', return_value=0.1):
            self.sensor_manager.startManager()
            time.sleep(0.25)
            self.sensor_manager.stopManager()

            test_data = self.sensor_manager.get_telemetry()
            self.assertIn('moisture_sensor', test_data)
            sensor_value, timestamp = test_data['moisture_sensor']
            self.assertIsInstance(sensor_value, tuple)
            self.assertGreaterEqual(len(sensor_value), 1)
            self.assertGreaterEqual(sensor_value[0], ConfigUtil.sensor_parser('moisture_sensor', 'min_val'))
            self.assertLessEqual(sensor_value[0], ConfigUtil.sensor_parser('moisture_sensor', 'max_val'))
            self.assertIsNotNone(timestamp)

    @unittest.skipUnless(ConfigUtil.use_hardware(), "Hardware disabled in config.json")
    def test_led_receives_hardware_data_within_moisture_range(self):
        self.sensor_manager.execute_read(self.sensor_manager.m_sensor)
        test_data = self.sensor_manager.get_telemetry()

        self.assertIn('moisture_sensor', test_data)
        sensor_value, _ = test_data['moisture_sensor']
        self.assertIsInstance(sensor_value, tuple)
        self.assertGreaterEqual(len(sensor_value), 1)

        new_led_val = sensor_value[0]
        self.assertGreaterEqual(new_led_val, ConfigUtil.sensor_parser('moisture_sensor', 'min_val'))
        self.assertLessEqual(new_led_val, ConfigUtil.sensor_parser('moisture_sensor', 'max_val'))

        self.led.updateLedColor(new_led_val)
        self.assertIsInstance(self.led.led.color, tuple)
        self.assertEqual(len(self.led.led.color), 3)
        self.assertTrue(all(isinstance(c, (int, float)) for c in self.led.led.color))

    def tearDown(self):
        pass 