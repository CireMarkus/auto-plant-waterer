import logging
import asyncio
import threading
import random
import sys
from typing import Any, Union
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="TestServer"+__name__)

trigger: Union[asyncio.Event, threading.Event]
trigger = threading.Event() if sys.platform in ["darwin", "win32"] else asyncio.Event()



def temp_test_data():
    """Generate random temperature data."""
    return random.randint(0,100)  # Simulating a temperature value between 0 and 100}

def hum_test_data():
    """Generate random humidity data."""
    return random.randint(0,100)  # Simulating a humidity value between 0 and 100

def read_request(characteristic: BlessGATTCharacteristic):
    if characteristic.description == "Temperature":
        value = temp_test_data()
        characteristic.update_value(str(value).encode('utf-8'))
    elif characteristic.description == "Humidity":
        value = hum_test_data()
        characteristic.update_value(str(value).encode('utf-8'))
    else:
        value = 0  # Default value for unknown characteristics
        characteristic.update_value(str(value).encode('utf-8'))
    logger.debug(f"Reading {characteristic.description}: {value}")
    



char_flags = (
    GATTCharacteristicProperties.read
    | GATTCharacteristicProperties.write
    | GATTCharacteristicProperties.indicate
)
permissions = (
    GATTAttributePermissions.readable
)

service_name = "Plant Monitor Service"
service_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"

temp_char_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CE"
hum_char_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CF"

async def run(loop):
    trigger.clear()
    

    server = BlessServer(name=service_name, loop=loop)
    server.read_request_func = read_request
    
    #Add service
    await server.add_new_service(service_uuid)
    
    #Add characteristics to the service
    await server. add_new_characteristic(
        temp_char_uuid,
        char_flags,
        permissions,
        description="Temperature"
    )
    
    await server.add_new_characteristic(
        hum_char_uuid,
        char_flags,
        permissions,
        description="Humidity"
    )
    
    logger.debug(server.get_characteristic(temp_char_uuid))
    logger.debug(server.get_characteristic(hum_char_uuid))
    await server.start()
    logger.debug("Advertising")
    
    await trigger.wait()
    
    await asyncio.sleep(2)
    logger.debug("Updating")
    server.get_characteristic(temp_char_uuid)
    server.update_value(service_uuid, temp_char_uuid)
    server.get_characteristic(hum_char_uuid)
    server.update_value(service_uuid, hum_char_uuid)
    await asyncio.sleep(5)
    
    if(KeyboardInterrupt):
        logger.info("KeyboardInterrupt received, stopping server.")
        await server.stop()
    