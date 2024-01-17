import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi,cs)

channel = AnalogIn(mcp,MCP.P0)


lowestV = channel.voltage
highestV = channel.voltage
lowestADC = channel.value
highestADC = channel.value


def lowestVoltage(newV,newADC):
    global lowestV
    global lowestADC

    if(newV < lowestV):
        lowestV = newV
    if (newADC < lowestADC):
        lowestADC = newADC

def highestVoltage(newV, newADC):
    global highestV
    global highestADC

    if (newV > highestV):
        highestV = newV
    if (newADC > highestADC):
        highestADC = newADC
try:
    while True:
        print('Raw ADC Value: ', channel.value)
        print('ADC Voltage: '+ str(channel.voltage)+ 'V')

        lowestVoltage(channel.voltage, channel.value)
        highestVoltage(channel.voltage,channel.value)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print("\n\n\n\n\n")
print("Highest Voltage: {}\nLowest Voltage: {}\nHighest ADC Value: {}\nLowest ADC Value: {}".format(highestV,lowestV,highestADC,lowestADC))
    
