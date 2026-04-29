import logging
import unittest
import time

from cda.Actuator.LED import LED

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