import logging
import busio 
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn
import json

import common.ConfigConst as ConfigConst
from cda.Sensor.BaseSensor import BaseSensor

class MoistureSensor(BaseSensor):

    def __init__(self, name, typeID, floor=None, ceiling=None):
        super().__init__(name, typeID, floor, ceiling)
        try:
            self.spi = buiso.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.cs  = digitalio.DigitalInOut(board.D8)
            self.mcp = MCP.MCP3008(self.spi,self.cs)
            self.channel = AnalogIn(mcp,MCP.P0)
            
        except Exception as e: 
            logging.error(f"The following error occurred while initializing {e}")
        

    #TODO: This function shall log the relative min and compare it to the absolute min. 
    def _calibrate(self):
        pass

    def getTelemetry(self) -> tuple:
        return (self.channel.value)