import logging 

from apscheduler.schedulers.background import BackgroundScheduler

import common.ConfigConst as ConfigConst
#from common.ConfigUtil import ConfigUtil

from cda.system.SystemUtilTasks import *

#from data.SystemPerformanceData import SystemPerformanceData

class SystemPeformanceManager(object):
    
    def __init__(self):
        #TODO:pull in or implement the config util here to find the config values for the device. 
        self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES #TODO: update to use the config util
        self.locationID = ConfigConst.NOT_SET #TODO: update to use the config util
        
        if self.pollRate <= 0: 
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
            
        self.dataMsgListener = None
        
        self.scheduler    = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate, coalesce=True)
        self.cpuTask      = SystemCpuUtilTask()
        self.memTask      = SystemMemUtilTask()
        self.diskTask     = SystemDiskUtilTask()
        self.netOutTask   = SystemNetOutUtilTask()
        
    # def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
    #     #TODO: implement the message listener
    #     pass 
    
    def startManager(self):
        logging.info("Starting System Performance Manager.....")
        
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("System Performance Manager Started.")
        else:
            logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")
            
    def stopManager(self): 
        logging.info("Stopping System Performance Manager....")
        try:
            self.scheduler.shutdown()
            logging.info("System Performance Manager Stopped.")
        except:
            logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring")
            
    def handleTelemetry(self):
        cpuUtilPct  = self.cpuTask.getTelemetryValue()
        memUtilPct  = self.memTask.getTelemetryValue()
        diskUtilPct = self.diskTask.getTelemetryValue()
        netOutPct   = self.netOutTask.getTelemetryValue()
        logging.debug(f'CPU utilization: {cpuUtilPct}%\n\
                        Memory utilization: {memUtilPct}%\n\
                        Disk utilization: {diskUtilPct}%\n\
                        NetOut utilization: {netOutPct}%')