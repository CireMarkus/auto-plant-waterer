"""
Configuration constants and other default values.
"""


NOT_SET = 'Not Set'
DEFAULT_TYPE_ID           =    0
DEFAULT_TYPE_CATEGORY_ID  =    0
DEFAULT_ACTUATOR_TYPE     = DEFAULT_TYPE_ID
DEFAULT_SENSOR_TYPE       = DEFAULT_TYPE_ID
DEFAULT_HOST             = 'localhost'
DEFAULT_COAP_PORT        = 5683
DEFAULT_COAP_SECURE_PORT = 5684
DEFAULT_MQTT_PORT        = 1883
DEFAULT_MQTT_SECURE_PORT = 8883
DEFAULT_RTSP_STREAM_PORT = 8554
DEFAULT_KEEP_ALIVE       = 60
DEFAULT_POLL_CYCLES      = 60
DEFAULT_VAL              = 0.0
DEFAULT_COMMAND          = 0
DEFAULT_STATUS           = 0
DEFAULT_TIMEOUT          = 5
DEFAULT_TTL              = 300
DEFAULT_QOS              = 0

DEFAULT_LAT = DEFAULT_VAL
DEFAULT_LON = DEFAULT_VAL
DEFAULT_ELEVATION = DEFAULT_VAL

DEFAULT_ACTION_ID = 0
INITIAL_SEQUENCE_NUMBER = 0

DEFAULT_STREAM_FPS             =    30
DEFAULT_MIN_STREAM_FPS         =     8
DEFAULT_MAX_STREAM_FPS         =    60
DEFAULT_STREAM_FRAME_WIDTH     =  1440
DEFAULT_STREAM_FRAME_HEIGHT    =  1080
DEFAULT_MIN_MOTION_PIXELS_DIFF = 12000
DEFAULT_MAX_CACHED_FRAMES      =    10
DEFAULT_STREAM_PROTOCOL        = 'rtsp'
DEFAULT_STREAM_FPS = 30
DEFAULT_MIN_MOTION_PIXELS_DIFF = 10000
DEFAULT_STREAM_PROTOCOL = 'rtsp'

#System Util Constants
SYSTEM_PERF_TYPE          = 9000
CPU_UTIL_TYPE             = 9001
DISK_UTIL_TYPE            = 9002
MEM_UTIL_TYPE             = 9003
NET_IN_UTIL_TYPE          = 9004
NET_OUT_UTIL_TYPE         = 9005

CPU_UTIL_NAME     = 'DeviceCpuUtil'
DISK_UTIL_NAME    = 'DeviceDiskUtil'
MEM_UTIL_NAME     = 'DeviceMemUtil'
NET_IN_UTIL_NAME  = 'DeviceNetInUtil'
NET_OUT_UTIL_NAME = 'DeviceNetOutUtil'

#Sensor Constants
LIGHT_SENSOR_NAME = 'veml7700 lights sensor'
LIGHT_SENSOR_TYPE = 1
LIGHT_SENSOR_FLOOR = None
LIGHT_SENSOR_CEILING = None

PLANTMONITOR_DEVICE = "Plant Monitor"
DEVICE_ID_KEY          = 'deviceID'
DEVICE_LOCATION_ID_KEY = 'deviceLocationID'

#####
# Property Names
#

NAME_PROP        = 'name'
DEVICE_ID_PROP   = 'deviceID'
TYPE_CATEGORY_ID_PROP = 'typeCategoryID'
TYPE_ID_PROP     = 'typeID'
TIMESTAMP_PROP   = 'timeStamp'
HAS_ERROR_PROP   = 'hasError'
STATUS_CODE_PROP = 'statusCode'
LOCATION_ID_PROP = 'locationID'
LATITUDE_PROP    = 'latitude'
LONGITUDE_PROP   = 'longitude'
ELEVATION_PROP   = 'elevation'

COMMAND_PROP     = 'command'
STATE_DATA_PROP  = 'stateData'
VALUE_PROP       = 'value'
IS_RESPONSE_PROP = 'isResponse'

CPU_UTIL_PROP    = 'cpuUtil'
DISK_UTIL_PROP   = 'diskUtil'
MEM_UTIL_PROP    = 'memUtil'
NET_IN_UTIL_PROP = 'netInUtil'
NET_OUT_UTIL_PROP= 'netOutUtil' 

ACTION_ID_PROP             = 'actionID'
DATA_URI_PROP              = 'dataURI'
MESSAGE_PROP               = 'message'
ENCODING_NAME_PROP         = 'encodingName'
RAW_DATA_PROP              = 'rawData'
SEQUENCE_NUMBER_PROP       = 'seqNo'
USE_SEQUENCE_NUMBER_PROP   = 'useSeqNo'
SEQUENCE_NUMBER_TOTAL_PROP = 'seqNoTotal'

SEND_RESOURCE_NAME_PROP    = 'sendResourceName'
RECEIVE_RESOURCE_NAME_PROP = 'receiveResourceName'
IS_PING_PROP               = 'isPing'
