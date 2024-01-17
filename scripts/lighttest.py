import time 
import board
import adafruit_veml7700

i2c=board.I2C() # uses board.SCL and board.SDA
veml7700 = adafruit_veml7700.VEML7700(i2c)

while True:
    print("Ambient light:{} Lux: {} ".format(veml7700.light,veml7700.lux))
    
    time.sleep(0.2)
    
