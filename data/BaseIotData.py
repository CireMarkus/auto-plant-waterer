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
    
    def setElevation(self, val: float):
        self.elevation = val
    
    def setLatitude(self, val: float):
        self.latitude = val
        
    def setLongitude(self, val: float):
        self.longitude = val
        
    def setLocationID(self, idStr: str):
        if idStr: 
            self.locationID = idStr
            
    def setName(self, name: str):
        if name: 
            self.name = name
            
    def setStatusCode(self, val: int):
        self.statusCode = val 
        if val < 0: 
            self.hasError = True
            
    def setTypeID(self, val: int):
        self.typeID = val
    
    def updateData(self, data):
        if data and isinstance(data,BaseIotData):
            self.setName(data.getName())
            self.setTypeID(data.getTypeID())
            self.setStatusCode(data.getStatusCode())
            self.setElevation(data.getElevation())
            self.setLatitude(data.getLatitude())
            self.setLongitude(data.getLongitude())
            self.setLocationID(data.getLocationID())

            self.updateTimeStamp()

            self._handleUpdateData(data)
    
    def updateTimeStamp(self): 
        self.timeStamp = str(datetime.now(timezone.utc).isoformat())
        

    def __str__(self):
        return '{}={},{}={},{}={},{}={},{}={},{}={},{}={},{}={},{}={}'.format(
			ConfigConst.NAME_PROP, self.name,
			ConfigConst.TYPE_ID_PROP, self.typeID,
			ConfigConst.TIMESTAMP_PROP, self.timeStamp,
			ConfigConst.STATUS_CODE_PROP, self.statusCode,
			ConfigConst.HAS_ERROR_PROP, self.hasError,
			ConfigConst.LOCATION_ID_PROP, self.locationID,
			ConfigConst.ELEVATION_PROP, self.elevation,
			ConfigConst.LATITUDE_PROP, self.latitude,
			ConfigConst.LONGITUDE_PROP, self.longitude)
    
    def _handleUpdateData(self,data):
        pass