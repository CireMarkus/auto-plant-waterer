from TempHumSensor import TempHumSensor
import time

sensor = TempHumSensor()
while True:
    print(f"Temp: {sensor.getTempFarenheit():.2f}\n\n")
    print(f"Humidity: {sensor.getHumidity():.2f}\n\n")
    time.sleep(2)
