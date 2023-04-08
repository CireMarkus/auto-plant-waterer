import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D26)

runs = 0; 
successfulRuns = 0;
failedRuns = 0;

while runs < 100000:
    
    try:
        temp = dht.temperature * (9/5) +32
        hum = dht.humidity
        #print("Temperature(F): {}, Humidity: {}".format(temp,hum))
        successfulRuns += 1
    except Exception as error:
        #print(error)
        failedRuns += 1
        pass
    runs += 1
    print(runs,end='\r')
    
print ("Runs: {}, Successful Runs: {} {}%, Failed Runs: {} {}%".format(runs,successfulRuns,((successfulRuns/runs)*100),failedRuns,((failedRuns/runs)*100)))
    
    