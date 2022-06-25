import busio
import digitalio
import board
import mariadb
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class MoistureSensor:
    '''
    The init funciton initalizes the mcp3008 chip to start sending
    signals to the RaspaberryPi. example MoistureSensor(board.D5,MCP.P0)
    '''
    def __init__(self,GPIO_PIN, MCP_CHANNEL):
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(GPIO_PIN)
        self.mcp = MCP.MCP3008(self.spi,self.cs)
        self.channel = AnalogIn(self.mcp,MCP_CHANNEL)
    '''
    This funciton passes the collected values to the database.
    A date and time stamp will be added to the value and that value
    will be sent to the data base. 
    '''
    def toDataBase(self):
        pass
 