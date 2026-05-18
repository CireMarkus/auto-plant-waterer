import logging

class SimulatedLightSensor:
    """Simulated light sensor that pulls data from CSV via SampleProvider."""
    
    # constants to mirror the real sensor API (numeric values used for sensitivity math)
    ALS_25MS = 0.025
    ALS_50MS = 0.05
    ALS_100MS = 0.1
    ALS_200MS = 0.2
    ALS_400MS = 0.4
    ALS_800MS = 0.8

    ALS_GAIN_1_8 = 0.125
    ALS_GAIN_1_4 = 0.25
    ALS_GAIN_1 = 1.0
    ALS_GAIN_2 = 2.0

    def __init__(self):
        # Try to use sample provider; fall back to deterministic random if file missing
        from common.SampleProvider import SampleProvider
        try:
            self._provider = SampleProvider('light_sensor')
            self.light_integration_time = self.ALS_100MS
            self.light_gain = self.ALS_GAIN_1
            self._last_light = 0
            self._last_lux = 0.0
        except Exception as e:
            logging.error(f"Unable to initalize sample provider. {e}")
            
        

    def _next_sample(self):
        if self._provider is not None:
            try:
                v = self._provider.next()
                if isinstance(v, tuple) or isinstance(v, list):
                    # expect (raw, lux)
                    self._last_light = int(v[0])
                    try:
                        self._last_lux = float(v[1])
                    except Exception:
                        self._last_lux = float(self._last_light) * (self.light_gain * self.light_integration_time)
                    return
                else:
                    self._last_light = int(v)
                    self._last_lux = float(self._last_light) * (self.light_gain * self.light_integration_time)
                    return
            except Exception:
                pass

    @property
    def light(self):
        self._next_sample()
        return self._last_light

    @property
    def lux(self):
        # ensure sample updated
        if self._provider is None:
            self._next_sample()
        return self._last_lux
