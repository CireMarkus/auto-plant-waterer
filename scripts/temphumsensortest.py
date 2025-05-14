import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D26)

runs = 0; 
successfulRuns = 0;
failedRuns = 0;
errors = []


while runs < 100:
    print("Run: {}".format(runs))
    time.sleep(3)
    try:
        print("Attempting to read DHT22 sensor")
        temp = dht.temperature * (9/5) +32
        hum = dht.humidity
        print("Temperature(F): {}, Humidity: {}".format(temp,hum))
        successfulRuns += 1
    except Exception as error:
        print("Failed to read DHT22 sensor")
        errors.append(error)
    runs+=1

print("\n\n\n\n\n\n\n\n\n") 
for i in errors:
    print(i)
    
    