
import logging


class BaseSensor:
    
    def __init_(self, name, typeID, floor = None, ceiling = None) -> None: 
        self.name = name
        self.typeID = typeID
        self.floor = floor
        self.ceiling = ceiling

    def getTelemetry(self) -> tuple:
        pass 

    def getName(self) -> str:
        return self.name
    
    def getTypeID(self) -> int:
        return self.typeID
    
    def getFloot(self) -> float:
        if self.floor:
            return self.floor
        logging.warning(f"Floor value for {self.name} was not set.")
    def getCeiling(self) -> float: 
        if self.ceiling:
            return self.ceiling
        logging.warning(f"Ceiling value for {self.name} was not set.")
    

    

    