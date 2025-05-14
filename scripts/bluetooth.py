import sys 
import logging 
import asyncio
import threading
import time
import random


from typing import Any, Union

from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)


 # Define a function to update the characteristics
def update_characteristics():
    while True:
        # Read the temperature and humidity from the sensor
        temp = random.uniform(60,80)
        humidity = sensor.uniform(30,50)
        print(f"Temperature: {temp} F, Humidity: {humidity} %")
        
        # Update the characteristics with the new values
        temp_characteristic.value = str(temp).encode("utf-8")
        humidity_characteristic.value = str(humidity).encode("utf-8")
        
        # Notify connected clients of the new values
        temp_characteristic.notify()
        humidity_characteristic.notify()
        
        # Sleep for a while before updating again
        time.sleep(2.5)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Create a TempHumSensor instance
    
    # Create a BlessServer instance
    server = BlessServer('BLE Test Server')
    
    # Define the UUIDs for the characteristics
    TEMP_UUID = "00001809-0000-1000-8000-00805f9b34fb"
    HUMIDITY_UUID = "00001809-0000-1000-8000-00805f9b34fc"
    
    # Define the properties and permissions for the characteristics
    TEMP_PROPERTIES = GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify
    HUMIDITY_PROPERTIES = GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify
    
    TEMP_PERMISSIONS = GATTAttributePermissions.readable
    HUMIDITY_PERMISSIONS = GATTAttributePermissions.readable
    
    # Create the temperature characteristic
    temp_characteristic = BlessGATTCharacteristic(
        uuid=TEMP_UUID,
        properties=TEMP_PROPERTIES,
        permissions=TEMP_PERMISSIONS,
        value=b"0",
    )
    # Create the humidity characteristic
    humidity_characteristic = BlessGATTCharacteristic(
        uuid=HUMIDITY_UUID,
        properties=HUMIDITY_PROPERTIES,
        permissions=HUMIDITY_PERMISSIONS,
        value=b"0",
    )
    # Add the characteristics to the server
    server.add_characteristic(temp_characteristic)
    server.add_characteristic(humidity_characteristic)
    # Start the server
    server.start()
    logger.info("BLE server started")
    logger.info(f"Current temperature: {sensor.getTempFarenheit()} F")
    logger.info(f"Current humidity: {sensor.getHumidity()} %")
   
    # Start a thread to update the characteristics
    update_thread = threading.Thread(target=update_characteristics)
    update_thread.daemon = True
    update_thread.start()
    # Run the server loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping BLE server")
        server.stop()
        sys.exit(0)
