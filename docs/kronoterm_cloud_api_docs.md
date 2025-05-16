# Table of Contents

* [client](#client)
  * [KronotermCloudApi](#client.KronotermCloudApi)
    * [\_\_init\_\_](#client.KronotermCloudApi.__init__)
    * [login](#client.KronotermCloudApi.login)
    * [get\_raw](#client.KronotermCloudApi.get_raw)
    * [post\_raw](#client.KronotermCloudApi.post_raw)
    * [update\_heat\_pump\_basic\_information](#client.KronotermCloudApi.update_heat_pump_basic_information)
    * [get\_initial\_data](#client.KronotermCloudApi.get_initial_data)
    * [get\_basic\_data](#client.KronotermCloudApi.get_basic_data)
    * [get\_system\_review\_data](#client.KronotermCloudApi.get_system_review_data)
    * [get\_heating\_loop\_data](#client.KronotermCloudApi.get_heating_loop_data)
    * [get\_alarms\_data](#client.KronotermCloudApi.get_alarms_data)
    * [get\_alarms\_data\_only](#client.KronotermCloudApi.get_alarms_data_only)
    * [get\_theoretical\_use\_data](#client.KronotermCloudApi.get_theoretical_use_data)
    * [get\_outside\_temperature](#client.KronotermCloudApi.get_outside_temperature)
    * [get\_working\_function](#client.KronotermCloudApi.get_working_function)
    * [get\_room\_temp](#client.KronotermCloudApi.get_room_temp)
    * [get\_reservoir\_temp](#client.KronotermCloudApi.get_reservoir_temp)
    * [get\_outlet\_temp](#client.KronotermCloudApi.get_outlet_temp)
    * [get\_sanitary\_water\_temp](#client.KronotermCloudApi.get_sanitary_water_temp)
    * [get\_heating\_loop\_target\_temperature](#client.KronotermCloudApi.get_heating_loop_target_temperature)
    * [get\_heating\_loop\_status](#client.KronotermCloudApi.get_heating_loop_status)
    * [get\_heating\_loop\_mode](#client.KronotermCloudApi.get_heating_loop_mode)
    * [get\_heat\_pump\_operating\_mode](#client.KronotermCloudApi.get_heat_pump_operating_mode)
    * [set\_heating\_loop\_mode](#client.KronotermCloudApi.set_heating_loop_mode)
    * [set\_heat\_pump\_operating\_mode](#client.KronotermCloudApi.set_heat_pump_operating_mode)
    * [set\_heating\_loop\_target\_temperature](#client.KronotermCloudApi.set_heating_loop_target_temperature)
    * [get\_theoretical\_power\_consumption](#client.KronotermCloudApi.get_theoretical_power_consumption)
* [kronoterm\_enums](#kronoterm_enums)
  * [HeatingLoop](#kronoterm_enums.HeatingLoop)
    * [HEATING\_LOOP\_1](#kronoterm_enums.HeatingLoop.HEATING_LOOP_1)
    * [HEATING\_LOOP\_2](#kronoterm_enums.HeatingLoop.HEATING_LOOP_2)
  * [APIEndpoint](#kronoterm_enums.APIEndpoint)
  * [WorkingFunction](#kronoterm_enums.WorkingFunction)
  * [HeatingLoopStatus](#kronoterm_enums.HeatingLoopStatus)
  * [HeatingLoopMode](#kronoterm_enums.HeatingLoopMode)
  * [HeatPumpOperatingMode](#kronoterm_enums.HeatPumpOperatingMode)
* [\_\_init\_\_](#__init__)

<a id="client"></a>

# client

<a id="client.KronotermCloudApi"></a>

## KronotermCloudApi Objects

```python
class KronotermCloudApi()
```

<a id="client.KronotermCloudApi.__init__"></a>

#### \_\_init\_\_

```python
def __init__(username: str, password: str)
```

Kronoterm heat pump cloud API.

**Arguments**:

- `username`: kronoterm cloud username
- `password`: kronoterm cloud password

<a id="client.KronotermCloudApi.login"></a>

#### login

```python
def login() -> None
```

Log in to cloud.

<a id="client.KronotermCloudApi.get_raw"></a>

#### get\_raw

```python
def get_raw(url: str, **kwargs) -> requests.Response
```

GET response from given url API endpoint.

**Arguments**:

- `url`: url of the request
- `kwargs`: any other arguments that will be passed to requests.get()

**Returns**:

response

<a id="client.KronotermCloudApi.post_raw"></a>

#### post\_raw

```python
def post_raw(url: str, **kwargs) -> requests.Response
```

POST response from given url API endpoint.

**Arguments**:

- `url`: url of the request
- `kwargs`: any other arguments that will be passed to requests.post()

**Returns**:

response

<a id="client.KronotermCloudApi.update_heat_pump_basic_information"></a>

#### update\_heat\_pump\_basic\_information

```python
def update_heat_pump_basic_information() -> None
```

Update heat pump information from INITIAL load data.

<a id="client.KronotermCloudApi.get_initial_data"></a>

#### get\_initial\_data

```python
def get_initial_data() -> dict[str, Any]
```

Get initial data.

**Returns**:

initial data

<a id="client.KronotermCloudApi.get_basic_data"></a>

#### get\_basic\_data

```python
def get_basic_data() -> dict[str, Any]
```

Get basic view data.

**Returns**:

basic view data

<a id="client.KronotermCloudApi.get_system_review_data"></a>

#### get\_system\_review\_data

```python
def get_system_review_data() -> dict[str, Any]
```

Get system review view data.

**Returns**:

system review data

<a id="client.KronotermCloudApi.get_heating_loop_data"></a>

#### get\_heating\_loop\_data

```python
def get_heating_loop_data(loop: HeatingLoop) -> dict[str, Any]
```

Get heating loop view data. Supports:

- HEATING_LOOP_1
- HEATING_LOOP_2
- TAP_WATER

**Returns**:

heating loop data

<a id="client.KronotermCloudApi.get_alarms_data"></a>

#### get\_alarms\_data

```python
def get_alarms_data() -> dict[str, Any]
```

Get alarm view data.

**Returns**:

alarm data

<a id="client.KronotermCloudApi.get_alarms_data_only"></a>

#### get\_alarms\_data\_only

```python
def get_alarms_data_only(
        alarms_data: dict[str, Any] | None = None) -> dict[str, Any]
```

Get only AlarmsData (list of alarms) part of the alarm response.

**Arguments**:

- `alarms_data`: if supplied it will be parsed for AlarmsData otherwise make API request

**Returns**:

list of alarms

<a id="client.KronotermCloudApi.get_theoretical_use_data"></a>

#### get\_theoretical\_use\_data

```python
def get_theoretical_use_data() -> dict[str, Any]
```

Get theoretical use view data. As displayed in 'Theoretical use histogram'.

**Returns**:

theoretical use data

<a id="client.KronotermCloudApi.get_outside_temperature"></a>

#### get\_outside\_temperature

```python
def get_outside_temperature() -> float
```

Get current outside temperature.

**Returns**:

outside temperature in [C]

<a id="client.KronotermCloudApi.get_working_function"></a>

#### get\_working\_function

```python
def get_working_function() -> WorkingFunction
```

Get currently set HP working function

**Returns**:

WorkingFunction Enum

<a id="client.KronotermCloudApi.get_room_temp"></a>

#### get\_room\_temp

```python
def get_room_temp() -> float
```

Get current room temperature.

**Returns**:

room temperature in [C]

<a id="client.KronotermCloudApi.get_reservoir_temp"></a>

#### get\_reservoir\_temp

```python
def get_reservoir_temp() -> float
```

Get current reservoir temperature.

**Returns**:

reservoir temperature in [C]

<a id="client.KronotermCloudApi.get_outlet_temp"></a>

#### get\_outlet\_temp

```python
def get_outlet_temp() -> float
```

Get current HP outlet temperature.

**Returns**:

HP outlet temperature in [C]

<a id="client.KronotermCloudApi.get_sanitary_water_temp"></a>

#### get\_sanitary\_water\_temp

```python
def get_sanitary_water_temp() -> float
```

Get current sanitary water temperature.

**Returns**:

sanitary water temperature in [C]

<a id="client.KronotermCloudApi.get_heating_loop_target_temperature"></a>

#### get\_heating\_loop\_target\_temperature

```python
def get_heating_loop_target_temperature(loop: HeatingLoop) -> float
```

Get currently set heating loop target temperature.

**Returns**:

currently set heating loop target temperature in [C]

<a id="client.KronotermCloudApi.get_heating_loop_status"></a>

#### get\_heating\_loop\_status

```python
def get_heating_loop_status(loop: HeatingLoop) -> HeatingLoopStatus
```

Get HP working status.

- ECO
   - NORMAL
   - COMFORT
   - OFF
   - AUTO

**Returns**:

HP working status

<a id="client.KronotermCloudApi.get_heating_loop_mode"></a>

#### get\_heating\_loop\_mode

```python
def get_heating_loop_mode(loop: HeatingLoop) -> HeatingLoopMode
```

Get the mode of heating loop:

- ON
   - OFF
   - AUTO

**Arguments**:

- `loop`: for which loop to get mode

**Returns**:

`mode`: mode of the loop

<a id="client.KronotermCloudApi.get_heat_pump_operating_mode"></a>

#### get\_heat\_pump\_operating\_mode

```python
def get_heat_pump_operating_mode() -> HeatPumpOperatingMode
```

Get the mode of heating loop:

- COMFORT
   - AUTO
   - ECO

**Returns**:

`mode`: mode of the heat pump

<a id="client.KronotermCloudApi.set_heating_loop_mode"></a>

#### set\_heating\_loop\_mode

```python
def set_heating_loop_mode(loop: HeatingLoop, mode: HeatingLoopMode) -> bool
```

Set the mode of heating loop:

- ON
   - OFF
   - AUTO

**Arguments**:

- `loop`: for which loop to set mode
- `mode`: mode of the loop

<a id="client.KronotermCloudApi.set_heat_pump_operating_mode"></a>

#### set\_heat\_pump\_operating\_mode

```python
def set_heat_pump_operating_mode(mode: HeatPumpOperatingMode) -> bool
```

Set the heat pump operating mode:

- COMFORT
   - AUTO
   - ECO

**Arguments**:

- `mode`: mode of the heat pump

<a id="client.KronotermCloudApi.set_heating_loop_target_temperature"></a>

#### set\_heating\_loop\_target\_temperature

```python
def set_heating_loop_target_temperature(loop: HeatingLoop,
                                        temperature: int | float) -> bool
```

Set heating loop temperature.

**Arguments**:

- `loop`: for which loop to set temperature
- `temperature`: temperature to set

<a id="client.KronotermCloudApi.get_theoretical_power_consumption"></a>

#### get\_theoretical\_power\_consumption

```python
def get_theoretical_power_consumption() -> namedtuple
```

Get theoretically calculated power consumption (calculated by HP and/or cloud).

**Returns**:

named tuple with latest daily power consumption in [kWh]

<a id="kronoterm_enums"></a>

# kronoterm\_enums

<a id="kronoterm_enums.HeatingLoop"></a>

## HeatingLoop Objects

```python
class HeatingLoop(IntEnum)
```

Heat pump heating loops

<a id="kronoterm_enums.HeatingLoop.HEATING_LOOP_1"></a>

#### HEATING\_LOOP\_1

Radiators

<a id="kronoterm_enums.HeatingLoop.HEATING_LOOP_2"></a>

#### HEATING\_LOOP\_2

Convectors

<a id="kronoterm_enums.APIEndpoint"></a>

## APIEndpoint Objects

```python
class APIEndpoint(StrEnum)
```

API endpoints used to get data and set heat pump parameters

<a id="kronoterm_enums.WorkingFunction"></a>

## WorkingFunction Objects

```python
class WorkingFunction(IntEnum)
```

Heat pump working functions

<a id="kronoterm_enums.HeatingLoopStatus"></a>

## HeatingLoopStatus Objects

```python
class HeatingLoopStatus(IntEnum)
```

Heat pump heating loop status dictated by heat pump operating mode and schedule

<a id="kronoterm_enums.HeatingLoopMode"></a>

## HeatingLoopMode Objects

```python
class HeatingLoopMode(IntEnum)
```

Heat pump heating loop mode

<a id="kronoterm_enums.HeatPumpOperatingMode"></a>

## HeatPumpOperatingMode Objects

```python
class HeatPumpOperatingMode(IntEnum)
```

Heat pump operating mode

<a id="__init__"></a>

# \_\_init\_\_

