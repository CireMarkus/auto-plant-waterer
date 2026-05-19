import logging
import threading
from apscheduler.schedulers.background import BackgroundScheduler

#custom libraries
import common.ConfigConst as ConfigConst
from common.ConfigUtil import ConfigUtil

from cda.Sensor.LightSensor import LightSensor
from cda.Sensor.MoistureSensor import MoistureSensor
from cda.Sensor.TempHumSensor import TempHumSensor

class SensorManager(object):
    
    def __init__(self):
        
        

        self.scheduler = BackgroundScheduler()
        self.hardware_bus_lock = threading.Lock()
        self.cache_lock = threading.Lock()

        #Sensor section
        self.m_sensor = MoistureSensor()
        self.l_sensor = LightSensor()
        self.th_sensor = TempHumiditySensor()

        #Sensor State Cache
        self.data_cache = {
            self.m_sensor.getName():  {},
            self.l_sensor.getName():  {},
            self.th_sensor.getName(): {}
        }


    def startManager(self):
        logging.info("Starting Sensor Manager.....")

        self.scheduler.add_job(lambda m=self.m_sensor: self.execute_read(m),
                                'interval', 
                                seconds=ConfigUtil.get_poll_rate("moisture_sensor"),
                                id=f"job_{self.m_sensor.getName()}",
                                max_instances=1)
        
        self.scheduler.add_job(lambda l=self.l_sensor: self.execute_read(l),
                                'interval', 
                                seconds=ConfigUtil.get_poll_rate("light_sensor"),
                                id=f"job_{self.l_sensor.getName()}",
                                max_instances=1)
        
        """self.scheduler.add_job(lambda th=self.th_sensor: self.execute_read(th),
                                    'interval', 
                                    seconds=ConfigUtil.get_poll_rate("temp_humidity_sensor"),
                                    id=f"job_{self.th_sensor.getName()}",
                                    max_instances=1)"""
        
        #NOTE: add subsequent sensors here.
        try:
            logging.debug("Starting sensor scheduler")
            self.scheduler.start()
        except Exception as e:
            logging.error(f"An error occured when starting the scheduler: {e}")
        logging.info("Sensor Manager has started")


    def stopManager(self):
        logging.info("Stopping Sensor Manager....")
        self.scheduler.shutdown()
        logging.info("Sensor Manager has stopped")
    
    def execute_read(self,sensor):
        """Background thread worker that updates 
            the central cache of sensor data."""

        with self.hardware_bus_lock: 
            try: 
                sensor_data = sensor.getTelemetry()[0]
            except Exception as e: 
                logging.error(f"Hardware error on {sensor.getName()}: {e}")
                return 
            
        with self.cache_lock:
            self.data_cache[sensor.getName()] = sensor_data
    
    def get_telemetry(self) -> dict:
        """
        Any other managers can call this at 
        any time to pull a snapshot of the most up-to-date data.
        """
        with self.cache_lock:
            """Return a copy of the dictionary so the caller doesn't 
            accidentally manipulate our live background cache"""
            return self.data_cache.copy()


        