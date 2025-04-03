from enum import Enum


class HeatingLoop(Enum):
    HEATING_LOOP_1 = 1  # Radiators
    HEATING_LOOP_2 = 2  # Convectors
    TAP_WATER = 5


class APIEndpoint(Enum):
    INITIAL = "Menu=1"
    BASIC = "TopPage=1&Subpage=1"
    SYSTEM_REVIEW = "TopPage=1&Subpage=2"
    SHORTCUTS = "TopPage=1&Subpage=3"
    HEATING_LOOP_1 = "TopPage=1&Subpage=5"
    HEATING_LOOP_1_SET = "TopPage=1&Subpage=5&Action=1"
    HEATING_LOOP_2 = "TopPage=1&Subpage=6"
    HEATING_LOOP_2_SET = "TopPage=1&Subpage=6&Action=1"
    TAP_WATER = "TopPage=1&Subpage=9"
    TAP_WATER_SET = "TopPage=1&Subpage=9&Action=1"
    ALARMS = "TopPage=1&Subpage=11"

    ADVANCED_SETTINGS = "TopPage=3&Subpage=11&Action=1"

    # TIMELINE_GRAPH = "TopPage=4&Subpage=1&Action=3"
    # CONSUMPTION_HISTOGRAM = "TopPage=4&Subpage=4&Action=4"


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


class HeatingLoopStatus(Enum):
    CIRCUIT_STATUS_OFF = 0
    CIRCUIT_STATUS_NORMAL = 1
    CIRCUIT_STATUS_ECO = 2
    CIRCUIT_STATUS_COMFORT = 3
    CIRCUIT_STATUS_AUTO = 4


class HeatingLoopMode(Enum):
    OFF = 0
    ON = 1
    AUTO = 2


class HeatPumpOperatingMode(Enum):
    AUTO = 0
    ECO = 1
    COMFORT = 2
