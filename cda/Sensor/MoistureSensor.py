import logging
import json

import common.ConfigConst as ConfigConst
from cda.Sensor.BaseSensor import BaseSensor
from cda.Sensor.SimulatedMoistureChannel import SimulatedMoistureChannel
import common.ConfigUtil as ConfigUtil


# Try to import hardware-specific libraries only when available. The final
# decision to use hardware also consults the `common/config.json` file via
# `ConfigUtil.use_hardware(...)` so CI/local runs can opt into simulation.
_LIBS_AVAILABLE = True
try:
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
except Exception:
    _LIBS_AVAILABLE = False


class MoistureSensor(BaseSensor):

    def __init__(self, name, typeID, floor=None, ceiling=None):
        super().__init__(name, typeID, floor, ceiling)
        use_hw_cfg = ConfigUtil.use_hardware()
        if _LIBS_AVAILABLE and use_hw_cfg:
            try:
                self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
                self.cs = digitalio.DigitalInOut(board.D8)
                self.mcp = MCP.MCP3008(self.spi, self.cs)
                self.channel = AnalogIn(self.mcp, MCP.P0)
            except Exception as e:
                logging.error(f"Hardware init failed: {e}.")
                exit()
        else:
            logging.info("Using simulated moisture channel (config or missing libs)")
            self.channel = SimulatedMoistureChannel(seed=name)

    # TODO: This function shall log the relative min and compare it to the absolute min.
    def _calibrate(self):
        pass

    # returns the raw ADC pin value [0,65535]
    def getTelemetry(self) -> tuple:
        return (self.channel.value,)
    