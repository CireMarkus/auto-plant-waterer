import logging
import threading
from apscheduler.schedulers.background import BackgroundScheduler

#custom libraries
import common.ConfigConst as ConfigConst
from common.ConfigUtil import ConfigUtil
from cda.Sensor.LightSensor import LightSensor
from cda.Sensor.MoistureSensor import MoistureSensor

class SensorManager(object):
    
    def __init__(self):
        
        self.scheduler = BackgroundScheduler()
        self.hardware_bus_lock = threading.Lock()
        self.m_sensor = MoistureSensor()
        self.l_sensor = LightSensor()
        #self.th_sensor = TempHumiditySensor()

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

        logging.info("Sensor Manager has started")
    def stopManager(self):
        logging.info("Stopping Sensor Manager....")
        logging.info("Sensor Manager has stopped")
    
    def execute_read(self,sensor):
        pass

        