# Table of Contents

* [kronoterm\_cloud\_api](#kronoterm_cloud_api)
  * [KronotermCloudApi](#kronoterm_cloud_api.KronotermCloudApi)
    * [\_\_init\_\_](#kronoterm_cloud_api.KronotermCloudApi.__init__)
    * [login](#kronoterm_cloud_api.KronotermCloudApi.login)
    * [get\_raw](#kronoterm_cloud_api.KronotermCloudApi.get_raw)
    * [post\_raw](#kronoterm_cloud_api.KronotermCloudApi.post_raw)
    * [update\_heat\_pump\_basic\_information](#kronoterm_cloud_api.KronotermCloudApi.update_heat_pump_basic_information)
    * [get\_initial\_data](#kronoterm_cloud_api.KronotermCloudApi.get_initial_data)
    * [get\_basic\_data](#kronoterm_cloud_api.KronotermCloudApi.get_basic_data)
    * [get\_system\_review\_data](#kronoterm_cloud_api.KronotermCloudApi.get_system_review_data)
    * [get\_heating\_loop\_data](#kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_data)
    * [get\_alarms\_data](#kronoterm_cloud_api.KronotermCloudApi.get_alarms_data)
    * [get\_alarms\_data\_only](#kronoterm_cloud_api.KronotermCloudApi.get_alarms_data_only)
    * [get\_outside\_temperature](#kronoterm_cloud_api.KronotermCloudApi.get_outside_temperature)
    * [get\_working\_function](#kronoterm_cloud_api.KronotermCloudApi.get_working_function)
    * [get\_room\_temp](#kronoterm_cloud_api.KronotermCloudApi.get_room_temp)
    * [get\_reservoir\_temp](#kronoterm_cloud_api.KronotermCloudApi.get_reservoir_temp)
    * [get\_outlet\_temp](#kronoterm_cloud_api.KronotermCloudApi.get_outlet_temp)
    * [get\_sanitary\_water\_temp](#kronoterm_cloud_api.KronotermCloudApi.get_sanitary_water_temp)
    * [get\_heating\_loop\_target\_temperature](#kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_target_temperature)
    * [get\_heating\_loop\_status](#kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_status)
    * [get\_heating\_loop\_mode](#kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_mode)
    * [set\_heating\_loop\_mode](#kronoterm_cloud_api.KronotermCloudApi.set_heating_loop_mode)
    * [set\_heating\_loop\_target\_temperature](#kronoterm_cloud_api.KronotermCloudApi.set_heating_loop_target_temperature)
* [kronoterm\_enums](#kronoterm_enums)
  * [HeatingLoop](#kronoterm_enums.HeatingLoop)
    * [HEATING\_LOOP\_1](#kronoterm_enums.HeatingLoop.HEATING_LOOP_1)
    * [HEATING\_LOOP\_2](#kronoterm_enums.HeatingLoop.HEATING_LOOP_2)
* [\_\_init\_\_](#__init__)

<a id="kronoterm_cloud_api"></a>

# kronoterm\_cloud\_api

<a id="kronoterm_cloud_api.KronotermCloudApi"></a>

## KronotermCloudApi Objects

```python
class KronotermCloudApi()
```

<a id="kronoterm_cloud_api.KronotermCloudApi.__init__"></a>

#### \_\_init\_\_

```python
def __init__(username: str, password: str)
```

Kronoterm heat pump cloud API.

**Arguments**:

- `username`: kronoterm cloud username
- `password`: kronoterm cloud password

<a id="kronoterm_cloud_api.KronotermCloudApi.login"></a>

#### login

```python
def login()
```

Log in to cloud.

<a id="kronoterm_cloud_api.KronotermCloudApi.get_raw"></a>

#### get\_raw

```python
def get_raw(url: str, **kwargs)
```

GET response from given url API endpoint.

**Arguments**:

- `url`: url of the request
- `kwargs`: any other arguments that will be passed to requests.get()

**Returns**:

response

<a id="kronoterm_cloud_api.KronotermCloudApi.post_raw"></a>

#### post\_raw

```python
def post_raw(url, **kwargs)
```

POST response from given url API endpoint.

**Arguments**:

- `url`: url of the request
- `kwargs`: any other arguments that will be passed to requests.post()

**Returns**:

response

<a id="kronoterm_cloud_api.KronotermCloudApi.update_heat_pump_basic_information"></a>

#### update\_heat\_pump\_basic\_information

```python
def update_heat_pump_basic_information()
```

Update heat pump information from INITIAL load data.

<a id="kronoterm_cloud_api.KronotermCloudApi.get_initial_data"></a>

#### get\_initial\_data

```python
def get_initial_data() -> dict
```

Get initial data.

**Returns**:

initial data

<a id="kronoterm_cloud_api.KronotermCloudApi.get_basic_data"></a>

#### get\_basic\_data

```python
def get_basic_data() -> dict
```

Get basic view data.

**Returns**:

basic view data

<a id="kronoterm_cloud_api.KronotermCloudApi.get_system_review_data"></a>

#### get\_system\_review\_data

```python
def get_system_review_data() -> dict
```

Get system review view data.

**Returns**:

system review data

<a id="kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_data"></a>

#### get\_heating\_loop\_data

```python
def get_heating_loop_data(loop: HeatingLoop) -> dict
```

Get heating loop view data. Supports:

- HEATING_LOOP_1
- HEATING_LOOP_2
- TAP_WATER

**Returns**:

heating loop data

<a id="kronoterm_cloud_api.KronotermCloudApi.get_alarms_data"></a>

#### get\_alarms\_data

```python
def get_alarms_data() -> dict
```

Get alarm view data.

**Returns**:

alarm data

<a id="kronoterm_cloud_api.KronotermCloudApi.get_alarms_data_only"></a>

#### get\_alarms\_data\_only

```python
def get_alarms_data_only(alarms_data: dict | None = None) -> dict
```

Get only AlarmsData (list of alarms) part of the alarm response.

**Arguments**:

- `alarms_data`: if supplied it will be parsed for AlarmsData otherwise make API request

**Returns**:

list of alarms

<a id="kronoterm_cloud_api.KronotermCloudApi.get_outside_temperature"></a>

#### get\_outside\_temperature

```python
def get_outside_temperature() -> float
```

Get current outside temperature.

**Returns**:

outside temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_working_function"></a>

#### get\_working\_function

```python
def get_working_function() -> WorkingFunction
```

Get currently set HP working function

**Returns**:

WorkingFunction Enum

<a id="kronoterm_cloud_api.KronotermCloudApi.get_room_temp"></a>

#### get\_room\_temp

```python
def get_room_temp() -> float
```

Get current room temperature.

**Returns**:

room temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_reservoir_temp"></a>

#### get\_reservoir\_temp

```python
def get_reservoir_temp() -> float
```

Get current reservoir temperature.

**Returns**:

reservoir temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_outlet_temp"></a>

#### get\_outlet\_temp

```python
def get_outlet_temp() -> float
```

Get current HP outlet temperature.

**Returns**:

HP outlet temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_sanitary_water_temp"></a>

#### get\_sanitary\_water\_temp

```python
def get_sanitary_water_temp() -> float
```

Get current sanitary water temperature.

**Returns**:

sanitary water temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_target_temperature"></a>

#### get\_heating\_loop\_target\_temperature

```python
def get_heating_loop_target_temperature(loop: HeatingLoop) -> float
```

Get currently set heating loop target temperature.

**Returns**:

currently set heating loop target temperature in [C]

<a id="kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_status"></a>

#### get\_heating\_loop\_status

```python
def get_heating_loop_status(loop: HeatingLoop) -> HeatingLoopStatus
```

Get HP working status.

**Returns**:

HP working status

<a id="kronoterm_cloud_api.KronotermCloudApi.get_heating_loop_mode"></a>

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

<a id="kronoterm_cloud_api.KronotermCloudApi.set_heating_loop_mode"></a>

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

<a id="kronoterm_cloud_api.KronotermCloudApi.set_heating_loop_target_temperature"></a>

#### set\_heating\_loop\_target\_temperature

```python
def set_heating_loop_target_temperature(loop: HeatingLoop,
                                        temperature: int | float) -> bool
```

Set heating loop temperature.

**Arguments**:

- `loop`: for which loop to set temperature
- `temperature`: temperature to set

<a id="kronoterm_enums"></a>

# kronoterm\_enums

<a id="kronoterm_enums.HeatingLoop"></a>

## HeatingLoop Objects

```python
class HeatingLoop(Enum)
```

<a id="kronoterm_enums.HeatingLoop.HEATING_LOOP_1"></a>

#### HEATING\_LOOP\_1

Radiators

<a id="kronoterm_enums.HeatingLoop.HEATING_LOOP_2"></a>

#### HEATING\_LOOP\_2

Convectors

<a id="__init__"></a>

# \_\_init\_\_

