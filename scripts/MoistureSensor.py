import busio
import digitalio
import board
import csv
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class MoistureSensor:
    
    #private members of the class used to initalize the sensor. 
    __spi = None
    __cs = None
    __mcp = None
    __channel = None
    __file = None
    __highestVoltage = 0.0 # higher voltage means less water in the pot. 
    __lowestVoltage = 0.0 # the lower the voltage the more water is in the pot.


    def __init__(self):
        
        #pin setting for the raspberry pi board. 
        try:
            self.__spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.__cs = digitalio.DigitalInOut(board.D5)
            self.__mcp = MCP.MCP3008(self.__spi,self.__cs)
            self.__channel = AnalogIn(self.__mcp,MCP.P0) 
        except: 
            print("There was an error initalizing the sensor/chip. Please check the connections.\n\n")
            
        """Will try to read max and min voltage from a file if there is one. 
            If there is no file the max and min voltage will be set to zero and 
            the user will be sent through the calibration process for the sensor. 
        """
        try: 
            self.__file = open("bounds.csv",'r')
            self.setBounds()
        except FileNotFoundError:
            print("File not found so max and min values will need to be set.\n")
            print("Calibraiton will run. Please have dry soil and water to set the moisture bounds.\n")
            self.calibrate()
    
    def calibrate(self): 
        self.__file = open("bounds.csv","w")
        values = []
        print("First we will be testing for the dryness of the soil.\n")
        #TODO find a way to run a while loop that waits for a button press.
        #TODO write highest and lowest voltage and ADC to a file. 

    #pulls from the .csv file and sets the voltage bounds for the moisture level. 
    def setBounds(self):
        csvReader = csv.reader(self.__file)
        values = []
        for col in csvReader: 
            values.append(col)
        
        self.__highestVoltage = values[0]
        self.__lowestVoltage = values[1]
        self.__file.close()
        self.__file = None

    #returns the ADC value and the voltage from the moisture sensor. 
    def moistureLevel(self):
        return (self.__channel.voltage,self.__channel.value)


def main():
    pass

if __name__ == '__main__':
    main()