import logging
from common.SampleProvider import SampleProvider


class SimulatedTempHumSensor:

    def __init__(self):
        try:
            self.provider = SampleProvider("temphum_sensor")
            self.last_temp = None
            self.last_hum = None
        except Exception as e:
            logging.error(f"Unable to initialize sample provider. {e}")
            self.provider = None
            self.last_temp = None
            self.last_hum = None

    def _read_sample(self):
        if self.provider is None:
            raise RuntimeError("SimulatedTempHumSensor has no sample provider")

        val = self.provider.next()
        if isinstance(val, (tuple, list)):
            self.last_temp = float(val[0])
            self.last_hum = float(val[1])
        else:
            raise ValueError(f"Expected tuple sample for temp/humidity sensor, got: {val}")

    @property
    def temperature(self):
        if self.last_temp is None or self.last_hum is None:
            self._read_sample()
        return self.last_temp

    @property
    def relative_humidity(self):
        if self.last_temp is None or self.last_hum is None:
            self._read_sample()
        return self.last_hum
