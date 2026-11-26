import logging
import threading

#custom libraries
import common.ConfigConst as ConfigConst #FIXME: review and see if this need to stay
import common.ConfigUtil as ConfigUtil

from cda.Actuator.LED import LED

class ActuatorManager:
    def __init__(self, sensor_manager=None):
        self._started = False

    def start_manager(self):
        #When the manager starts it should initalize all 
        # the actuators to make sure they work. 

        try: 
            self.led = LED(ConfigUtil.sensor_parser("moisture_sensor","min_val"),ConfigUtil.sensor_parser("moisture_sensor","max_val"))
        except Exception as e:
            logging.exception("There was an error when initalizing the actuator",e)
            
        logging.info("The actuator manager has started....")

    def stop_manager(self):

        logging.info("The actuator manager has stopped....")
        pass

    def get_sensor_data(self,sensor_name):
        '''
        This function should in theory get the data from the sensor manager
        I'm to quite sure how it will do that but once the data has been updated 
        on the sensor manager this should be called for the associated actuator and 
        the actuator should take action on that data. 
        '''
        pass