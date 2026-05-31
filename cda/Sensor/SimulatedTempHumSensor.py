import logging
from common.SampleProvider import SampleProvider



class SimulatedTempHumSensor:
    
    def __init__(self):
        try: 
            self.provider = SampleProvider("temphum_sensor")
            self.last_temp = 0.0 
            self.last_hum = 0.0 
        except Exception as e: 
            logging.error(f"Unable to initalize sample provider. {e}")

    def next_sample(self):
        val = self.provider.next()
        
        if isinstance(val,tuple) or isisntance(val,list): 
            self.last_temp = float(val[0])
            self.last_hum = float(val[1])
    
    
    @property
    def temperature(self):
        self.next_sample()
        return self.last_temp
    
    @property
    def relative_humidity(self):
        self.next_sample()
        return self.last_hum
