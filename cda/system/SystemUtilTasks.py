import psutil
import time

import common.ConfigConst as ConfigConst

class BaseSystemUtilTask():

    def __init__(self, name = ConfigConst.NOT_SET, typeID = ConfigConst.DEFAULT_SENSOR_TYPE):
        self.name = name 
        self.typeID = typeID
        
    def getName (self) -> str: 
        return self.name
    
    def getTypeID(self) -> int:
        return self.typeID
    
    def getTelemetryValue(self) -> float:
        pass

class SystemCpuUtilTask(BaseSystemUtilTask):
    """
    Class to reutrn CPU performance data.
    """
    
    def __init__(self):
        super(SystemCpuUtilTask,self).__init__(name=ConfigConst.CPU_UTIL_NAME, typeID=ConfigConst.CPU_UTIL_TYPE)
    
    def getTelemetryValue(self) -> float:
        return (psutil.cpu_percent())

class SystemMemUtilTask(BaseSystemUtilTask):
    """
    Class to return system memory statistics.
    """
    
    def __init__(self):
        super(SystemMemUtilTask,self).__init__(name=ConfigConst.MEM_UTIL_NAME, typeID=ConfigConst.MEM_UTIL_TYPE)
    
    def getTelemetryValue(self) -> float:
        return psutil.virtual_memory().percent
    
class SystemDiskUtilTask(BaseSystemUtilTask):
    """
    Class to return the disk statistics. 
    """
    def __init__(self):
        super(SystemDiskUtilTask,self).__init__(name=ConfigConst.DISK_UTIL_NAME, typeID=ConfigConst.DISK_UTIL_TYPE)
    
    def getTelemetryValue(self) -> float:
        return psutil.disk_usage("/").percent

class SystemNetOutUtilTask(BaseSystemUtilTask):
    """
    Class to return the network utilization. 
    """
    
    def __init__(self):
        super(SystemNetOutUtilTask,self).__init__(name=ConfigConst.NET_OUT_UTIL_NAME , typeID=ConfigConst.NET_OUT_UTIL_TYPE)
    
    def getTelemetryValue(self)-> float:
        
        self.interval = 1
        stats_before = psutil.net_io_counters()
        bytes_sent_before = stats_before.bytes_sent
        
        time.sleep(self.interval)
        
        stats_after = psutil.net_io_counters()
        bytes_sent_after = stats_after.bytes_sent
        
        return (bytes_sent_after - bytes_sent_before)/self.interval
    