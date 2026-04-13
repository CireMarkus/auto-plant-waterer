from datetime import datetime, timezone 

import common.ConfigConst as ConfigConst
import common.ConfigUtil as ConfigUtil
"""
Base class to handle data that will be sent between the CDA device.
"""

class BaseIotData(object):
    
    
    
    def __init__(self, name = ConfigConst.NOT_SET, typeID = ConfigConst.DEFAULT_TYPE_ID, d = None):
        self.updateTimeStamp()
        self.hasError = False
        
        useDefaults = True
        
        if d: 
            try:
                self.name       = d[ConfigConst.NAME_PROP]
                self.typeID     = d[ConfigConst.TYPE_ID_PROP]
                self.statusCode = d[ConfigConst.STATUS_CODE_PROP]
                self.latitude   = d[ConfigConst.LATITUDE_PROP]
                self.longitude  = d[ConfigConst.LONGITUDE_PROP]
                self.elevation  = d[ConfigConst.ELEVATION_PROP]
				
                useDefaults = False
            except:
                pass
        if useDefaults: 
            self.name       = name
            self.typeID     = typeID
            self.statusCode = ConfigConst.DEFAULT_STATUS
            self.latitude   = ConfigConst.DEFAULT_LAT
            self.longitude  = ConfigConst.DEFAULT_LON
            self.elevation  = ConfigConst.DEFAULT_ELEVATION
        
        if not self.name: 
            self.name = ConfigConst.NOT_SET

        #always pull location ID from configuration file 
        self.locationID = ConfigUtil().getproperty(ConfigConst.PLANTMONITOR_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY)
    
    def getElevation(self) -> float: 
        return self.elevation
    
    def getLongitude(self) -> float: 
        return self.longitude

    def getLocationID(self) -> str:
        return self.locationID
    
    def getName(self) -> str:
        return self.name
    
    def getStatusCode(self) -> int:
        return self.statusCode
    
    def getTimeStamp(self) -> str:
        return self.timeStamp
    
    def getTypeID(self) -> int:
        return self.typeID
    
    def hasErrorFlag(self):
        return self.hasError
    
    def updateTimeStamp(self): 
        self.timeStamp = str(datetime.now(timezone.utc).isoformat())