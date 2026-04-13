"""
Configuration constants and other default values.
"""


NOT_SET = 'Not Set'
DEFAULT_SENSOR_TYPE = 0
DEFAULT_TYPE_ID = 0

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
