from os import system, name
import busio
import digitalio
import os
import board
import csv
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import keyboard
import time
import json

class MoistureSensor:
    
    #private members of the class used to initalize the sensor. 
    __spi = None
    __cs = None
    __mcp = None
    __channel = None
    __file = None
    __highestValue = 0 # higher adc value means less water in the pot
    __highestVoltage = 0.0 # higher voltage means less water in the pot. 
    __lowestVoltage = 0.0 # the lower the voltage the more water is in the pot.
    __lowestValue = 0 # lower adc value means more water in the pot. 
    __calibrateTime = 10.0 #variable to hold the time that the calibrations will run.
    __fileName = "Data/moistureBounds.txt"

    def __init__(self):
        
        #pin setting for the raspberry pi board. 
        try:
            self.__spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.__cs = digitalio.DigitalInOut(board.D5)
            self.__mcp = MCP.MCP3008(self.__spi,self.__cs)
            self.__channel = AnalogIn(self.__mcp,MCP.P0) 
        except: 
            print("There was an error initalizing the sensor/chip. Please check the connections.\n")
            quit()
        
        """Will try to read max and min voltage from a file if there is one. 
            If there is no file the max and min voltage will be set to zero and 
            the user will be sent through the calibration process for the sensor. 
        """
        try: 
            self.__file = open(self.__fileName,'r')
            print("File was located successfully. Now the bounds will be loaded.\n\n")
            self.__setBounds() 
        except FileNotFoundError:
            os.mkdir("Data")
            print("File not found so max and min values will need to be set.\n")
            print("Calibraiton will run. Please have dry soil and water to set the moisture bounds.\n")
            self.calibrate()
    
    def clear(self): 
        if name == 'nt':
            _ = system('cls')
        else: 
            _ = system('clear')

    def calibrate(self): 
        self.__file = open(self.__fileName,"w")
        values = []
        print("First we will be testing for the dryness of the soil.\n")
        print("Place the sensor in the dry soil and press enter to continue: \n")
        input("Press Enter to continue.")
        self.__highestVoltage = self.__channel.voltage
        self.__highestValue = self.__channel.value
        self.__lowestVoltage = self.__channel.voltage
        self.__lowestValue = self.__channel.value

        startTime = time.time()
        while True:
            #condition to set the variables as the highest value of the voltage 
            # sensor. 
            if(self.__highestVoltage < self.__channel.voltage):
                self.__highestVoltage = self.__channel.voltage 
            if(self.__highestValue < self.__channel.value):
                self.__highestValue = self.__channel.value
            print("Time running: {:.2f}, Highest value: {:.4f}".format((time.time() - startTime),self.__highestValue),end='\r')
            if ((time.time() - startTime) > self.__calibrateTime): 
                print('Ending calibration for soil dryness.\n\n')
                break
        self.clear()
        print("Next we will test test the wetness of the soil")
        
        values.append(self.__highestVoltage)
        values.append(self.__highestValue)
        input("Press Enter to continue.")
        startTime = time.time()
        while True: 
            if(self.__lowestVoltage > self.__channel.voltage):
                self.__lowestVoltage = self.__channel.voltage
            if(self.__lowestValue > self.__channel.value):
                self.__lowestValue = self.__channel.value
            print("Time running: {:.2f}, Lowest value: {:.4f}".format((time.time() - startTime),self.__lowestValue),end='\r')
            if ((time.time() -startTime) > self.__calibrateTime):
                print('Ending calibration for soil wetness.\n\n')
                break
        print("Calibration is complete.\n\n")
        self.clear()
        values.append(self.__lowestVoltage)
        values.append(self.__lowestValue)
        input("Press enter to continue.")
        
        json.dump(values,self.__file)
        self.__file.close()


    #pulls from the .csv file and sets the voltage bounds for the moisture level. 
    def __setBounds(self):
        values = json.load(self.__file)
        
        self.__highestVoltage = values[0]
        self.__highestValue = values[1]
        self.__lowestVoltage = values[2]
        self.__lowestValue = values[3]
        self.__file.close()
        
        print("Highest voltage:{} \nHighest ADC Value:{} \nLowest voltage:{} \nLowest ADC Value:{}".format(self.__highestVoltage,self.__highestValue,self.__lowestVoltage,self.__lowestValue))

    #returns the ADC value and the voltage from the moisture sensor. 
    def moistureLevel(self):
        return (self.__channel.voltage,self.__channel.value)
    
    #returns the upper and lower bound for the moisture levels
    def getUpperBound(self):
        return(self.__highestVoltage,self.__highestValue)
    
    def getLowerBound(self):
        return(self.__lowestVoltage,self.__lowestValue)

    def __del__(self):
        print("Moisture sensor deleted.")
        pass

