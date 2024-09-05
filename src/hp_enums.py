from enum import Enum


class WorkingFunction(Enum):
    HP_FUNCTION_HEATING = 0
    HP_FUNCTION_SANITARY_WATER_HEATING = 1
    HP_FUNCTION_COOLING = 2
    HP_FUNCTION_POOL_HEATING = 3
    HP_FUNCTION_ANTILEGIONELLA = 4
    HP_FUNCTION_SLEEP = 5
    HP_FUNCTION_STARTUP = 6
    HP_FUNCTION_REMOTE_DISCONNECT = 7
    HP_FUNCTION_ACTIVE_COMPRESSOR_SECURITY = 8


class APIEndpoint(Enum):
    SYSTEM_REVIEW = "TopPage=1&Subpage=2"
    HEATING_LOOP_2 = "TopPage=1&Subpage=6"
    TIMELINE_GRAPH = "TopPage=4&Subpage=1&Action=3"
    CONSUMPTION_HISTOGRAM = "TopPage=4&Subpage=4&Action=4"
    SET_HEATING_LOOP_2 = "TopPage=1&Subpage=6&Action=1"

class HeatingLoop(Enum):
    HIGH_TEMPERATURE_LOOP = 1  # Radiators
    LOW_TEMPERATURE_LOOP = 2   # Convectors

class HeatingLoopMode(Enum):
    OFF = 0
    ON = 1
    AUTO = 2