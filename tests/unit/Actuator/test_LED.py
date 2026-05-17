import colorsys
import importlib
import logging
import unittest
import time

import common.ConfigUtil as ConfigUtil
from cda.Actuator.LED import LED, _DummyRGBLED

class LedTest(unittest.TestCase):
    """
    Validate the LED color mapping based on moisture sensor input.
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Initializing LED Unit Test...")
        # Calibration: Wet=24000 (Ceiling), Dry=52000 (Floor)
        cls.led = LED(floor=24000, ceiling=52000)
    
    def testColorTransitions(self): 
        # Test 1: Simulate Bone Dry (Should be Red)
        logging.info("Simulating DRY soil...")
        self.led.updateLedColor(52000)
        self.assertAlmostEqual(self.led.moisture_perc, 0.0)
        time.sleep(1)

        # Test 2: Simulate Ideal Moisture (Should be Green)
        logging.info("Simulating PERFECT soil...")
        self.led.updateLedColor(38000)
        self.assertTrue(0.4 < self.led.moisture_perc < 0.6)
        time.sleep(1)

        # Test 3: Simulate Submerged (Should be Blue)
        logging.info("Simulating WET soil...")
        self.led.updateLedColor(24000)
        self.assertAlmostEqual(self.led.moisture_perc, 1.0)
        time.sleep(1)

    def testSweep(self):
        """Watch the LED smoothly transition from Red to Blue"""
        logging.info("Running smooth color sweep test...")
        for val in range(52000, 24000, -1000):
            self.led.updateLedColor(val)
            time.sleep(0.1)

    def testDummyLedFallback(self):
        logging.info("Testing fallback when LED hardware is unavailable...")
        dummy_led = LED(floor=24000, ceiling=52000, rgb_led_class=_DummyRGBLED)
        dummy_led.updateLedColor(38000)
        expected_color = colorsys.hsv_to_rgb(dummy_led.moisture_perc * 0.7, 1, 1)
        self.assertEqual(dummy_led.led.color, expected_color)

    def testConfigDisablesHardware(self):
        logging.info("Testing config-based LED hardware disable path...")
        original_use_hardware = ConfigUtil.use_hardware
        ConfigUtil.use_hardware = lambda *args, **kwargs: False
        try:
            led = LED(floor=24000, ceiling=52000)
            self.assertIsInstance(led.led, _DummyRGBLED)
        finally:
            ConfigUtil.use_hardware = original_use_hardware