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


class CustomBleakGATTDescriptor(bleak.backends.descriptor.BleakGATTDescriptor):
    """The Bleak representation of a GATT Descriptor"""

    def __init__(
        self, obj: Any, handle: int, uuid: str, characteristic: BlessGATTCharacteristic
    ):
        """
        Args:
            obj: The backend-specific object for the descriptor.
            handle: The handle of the descriptor.
            uuid: The UUID of the descriptor.
            characteristic: The characteristic that this descriptor belongs to.
        """
        self.obj = obj
        self._handle = handle
        self._uuid = uuid
        self._characteristic = characteristic

    def __str__(self):
        return f"{self.uuid} (Handle: {self.handle}): {self.description}"

    @property
    def characteristic_uuid(self) -> str:
        """UUID for the characteristic that this descriptor belongs to"""
        return self._characteristic.uuid

    @property
    def characteristic_handle(self) -> int:
        """handle for the characteristic that this descriptor belongs to"""
        return self._characteristic.handle

    @property
    def uuid(self) -> str:
        """UUID for this descriptor"""
        return self._uuid

    @property
    def handle(self) -> int:
        """Integer handle for this descriptor"""
        return self._handle

    @property
    def description(self) -> str:
        """A text description of what this descriptor represents"""
        return _descriptor_descriptions.get(self.uuid, ["Unknown"])[0]


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
    
    #Add descriptors to the characteristics
    server.get_characteristic(temp_char_uuid).add_descriptor(
        CustomBleakGATTDescriptor(
            handle=0x2901,  # User Description Descriptor
            uuid="2901",
            characteristic=server.get_characteristic(temp_char_uuid),
        )
    )
    
    server.get_characteristic(hum_char_uuid).add_descriptor(
        CustomBleakGATTDescriptor(
            handle=0x2902,  # User Description Descriptor
            uuid="2902",
            characteristic=server.get_characteristic(hum_char_uuid),
        )
    )
    # Set the description for the characteristics
    server.get_characteristic(temp_char_uuid).get_descriptor("2901").description = "Temperature Sensor"
    server.get_characteristic(hum_char_uuid).get_descriptor("2902").description = "Humidity Sensor"
    
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