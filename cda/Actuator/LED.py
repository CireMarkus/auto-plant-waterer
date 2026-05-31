import colorsys
import logging
from cda.Actuator.DummyRGBLED import DummyRBGLED

import common.ConfigUtil as ConfigUtil

try:
    from gpiozero import RGBLED # type: ignore
    _HARDWARE_AVAILABLE = True
except Exception:
    RGBLED = None
    _HARDWARE_AVAILABLE = False



class LED():
    def __init__(self, floor, ceiling, rgb_led_class=None):
        self.moisture_perc = 0
        self.cur_moisture = 0
        self.dry = ceiling # the higher value is the dry value
        self.wet = floor # the lower value is the wet value

        if rgb_led_class is None:
            use_hw = ConfigUtil.use_hardware()
            rgb_led_class = RGBLED if use_hw and _HARDWARE_AVAILABLE else DummyRBGLED 

        try:
            self.led = rgb_led_class(26, 19, 13)
        except Exception as e:
            logging.warning(f"LED hardware unavailable: {e}. Using dummy LED.")
            self.led = DummyRBGLED()

    def updateLedColor(self,value):
        self.cur_moisture = value
        self.moisture_perc = (self.dry - self.cur_moisture) / (self.dry - self.wet)

        hue = self.moisture_perc * 0.7
        r,g,b = colorsys.hsv_to_rgb(hue,1,1)
        self.led.color = (r,g,b)
        
        logging.debug(f"Raw: {value} | Perc: {self.moisture_perc:.2%} | RGB: {r:.2f},{g:.2f},{b:.2f}")
