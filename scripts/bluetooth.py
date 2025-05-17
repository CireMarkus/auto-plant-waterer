import time
import random
import threading
import logging

# Import the necessary classes from bless
from bless import (
    BlessServer,
    BlessGATTService,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)

# Set up logging for debugging and information
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple_ble_server")

# Define a unique UUID for the service
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Define a unique UUID for the random number characteristic
RANDOM_UUID = "12345678-1234-5678-1234-56789abcdef0"

# Set the characteristic properties and permissions
CHAR_PROPERTIES = GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify
CHAR_PERMISSIONS = GATTAttributePermissions.readable

# Create the BLE server instance
server = BlessServer(name="RandomNumberBLE")

# Create the service
service = BlessGATTService(SERVICE_UUID)

# Create the characteristic for transmitting random numbers
random_char = BlessGATTCharacteristic(
    uuid=RANDOM_UUID,
    properties=CHAR_PROPERTIES,
    permissions=CHAR_PERMISSIONS,
    value=b"0",  # Initial value as bytes
)

# Add the characteristic to the service
service.add_characteristic(random_char)

# Add the service to the server
server.add_service(service)

def update_random_number():
    """
    This function runs in a separate thread.
    It generates a new random number every 2 seconds,
    updates the BLE characteristic, and prints the value to the console.
    """
    while True:
        # Generate a random integer between 0 and 100
        rand_num = random.randint(0, 100)
        logger.info(f"Generated random number: {rand_num}")

        # Update the BLE characteristic value (must be bytes)
        random_char.value = str(rand_num).encode("utf-8")

        # Notify connected BLE clients of the new value
        random_char.notify()

        # Wait before generating the next number
        time.sleep(2)

if __name__ == "__main__":
    try:
        # Start the BLE server
        logger.info("Starting BLE server...")
        server.start()

        # Start the random number update thread
        updater = threading.Thread(target=update_random_number, daemon=True)
        updater.start()

        # Keep the main thread alive to maintain the BLE server
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down BLE server.")
        server.stop()