import logging
import asyncio
import threading
import random
import sys
from typing import Any, Union
import bleak.backends
import bleak.backends.descriptor
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)
import bleak


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="TestServer"+__name__)

trigger: Union[asyncio.Event, threading.Event]
trigger = threading.Event() if sys.platform in ["darwin", "win32"] else asyncio.Event()



def temp_test_data():
    """Generate random temperature data."""
    value = random.randint(0, 100)  # Simulating a temperature value between 0 and 100
    logger.debug(f"Generated temperature data: {value}")
    print(f"Generated temperature data: {value}")
    return  value # Simulating a temperature value between 0 and 100}

def hum_test_data():
    """Generate random humidity data."""
    value = random.randint(0, 100)  # Simulating a humidity value between 0 and 100
    logger.debug(f"Generated humidity data: {value}")
    print(f"Generated humidity data: {value}")
    return value # Simulating a humidity value between 0 and 100

def read_request(characteristic: BlessGATTCharacteristic, **kwargs: Any) -> bytearray:
    logger.debug(f"Reading {characteristic.description}: {characteristic.value}")
    print(f"Reading {characteristic.description}: {characteristic.value}")
    return characteristic.value
    



char_flags = (
    GATTCharacteristicProperties.read
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
    await server.add_new_characteristic(
        service_uuid,
        temp_char_uuid,
        char_flags,
        temp_test_data().to_bytes(2, 'little'),
        permissions
    )
    
    await server.add_new_characteristic(
        service_uuid,
        hum_char_uuid,
        char_flags,
        hum_test_data().to_bytes(2, 'little'),
        permissions
    )
    
    await server.get_characteristic(temp_char_uuid).add_descriptor(bleak.backends.descriptor.BleakGATTDescriptor(
        uuid="2901",  # Characteristic User Description UUID
        value=b"Temperature in Celsius",
        permissions=GATTAttributePermissions.readable
    ))
    await server.get_characteristic(hum_char_uuid).add_descriptor(bleak.backends.descriptor.BleakGATTDescriptor(
        uuid="2901",  # Characteristic User Description UUID
        value=b"Humidity in Percentage",
        permissions=GATTAttributePermissions.readable
    ))
    
    logger.debug(server.get_characteristic(temp_char_uuid))
    logger.debug(server.get_characteristic(hum_char_uuid))
    await server.start()
    logger.debug("Advertising")
    print("Advertising started. Press Ctrl+C to stop.")
    
    await trigger.wait()
    
    # await asyncio.sleep(2)
    logger.debug("Updating")
    print("Updating values...")
    server.get_characteristic(temp_char_uuid)
    await server.update_value(service_uuid, temp_char_uuid)
    server.get_characteristic(hum_char_uuid)
    await server.update_value(service_uuid, hum_char_uuid)
    # await asyncio.sleep(5)
    
    if(KeyboardInterrupt):
        logger.info("KeyboardInterrupt received, stopping server.")
        print("KeyboardInterrupt received, stopping server.")
        await server.stop()
    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))