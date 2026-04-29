from gpiozero import RGBLED 
from time import sleep
import colorsys
import logging 

class LED():
    def __init__(self, floor, ceiling):
        self.led = RGBLED(26,19,13)
        self.moisture_perc = 0 
        self.cur_moisture = 0
        self.dry = ceiling #the higher value is the dry value
        self.wet = floor #the lower value is the celing. 

    def updateLedColor(self,value):
        self.cur_moisture = value
        self.moisture_perc = (self.wet - self.cur_moisture) / (self.wet - self.dry)

        hue = self.moisture_perc * 0.7
        r,g,b = colorsys.hsv_to_rgb(hue,1,1)
        self.led.color = (r,g,b)
        
        logging.debug(f"Raw: {value} | Perc: {self.moisture_perc:.2%} | RGB: {r:.2f},{g:.2f},{b:.2f}")
