class SimulatedMoistureChannel:
    """Simulated moisture sensor channel that pulls data from CSV via SampleProvider."""
    
    def __init__(self, seed=None):
        # Try to use sample provider; fall back to deterministic random if file missing
        from common.SampleProvider import SampleProvider
        try:
            self._provider = SampleProvider('moisture_sensor')
        except Exception:
            self._provider = None

    @property
    def value(self):
        if self._provider is not None:
            try:
                return int(self._provider.next())
            except Exception:
                pass
        # ADC-like 16-bit range used by the real sensor wrapper
        return 0
