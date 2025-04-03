[![PyPI - Version](https://img.shields.io/pypi/v/kronoterm-cloud-api)](https://pypi.org/project/kronoterm-cloud-api/)
[![ruff](https://github.com/LeskoIam/kronoterm_cloud_api/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_api/actions/workflows/ruff.yml)

# Kronoterm cloud API (unofficial)

API client for controlling Kronoterm heat pumps via their cloud (cloud.kronoterm.com/).

## Installation

1. Install using `pip`
   ```shell
   python -m pip install kronoterm_cloud_api
   ```
2. Enjoy!


## Documentation
API documentation available [here](./docs/kronoterm_cloud_api_docs.md).

## Examples

```python
from kronoterm_cloud_api.client import KronotermCloudApi
from kronoterm_enums import HeatingLoop, HeatingLoopMode

hp_api = KronotermCloudApi("your-kronoterm-cloud-username", "your-kronoterm-cloud-password")
hp_api.login()

print(hp_api.get_room_temp())  # Current room temperature.
# >> 24.0
print(hp_api.get_outside_temperature())  # Current outside temperature.
# >> 23.4
print(hp_api.get_reservoir_temp())  # Current reservoir temperature.
# >> 11.4

print(hp_api.get_working_function())  # Currently set HP working function
# >> WorkingFunction.HP_FUNCTION_SLEEP
print(hp_api.get_heating_loop_mode(HeatingLoop.HEATING_LOOP_2))  # Get the mode of heating loop.
# >> HeatingLoopMode.AUTO

print(hp_api.set_heating_loop_target_temperature(HeatingLoop.HEATING_LOOP_2, 24))  # Set heating loop temperature.
# >> True
print(
    hp_api.set_heating_loop_mode(HeatingLoop.HEATING_LOOP_2, HeatingLoopMode.AUTO))  # Set the mode of heating loop.
# >> True

print(hp_api.get_theoretical_power_consumption())
# >> HPConsumption(heating=0.7924833333333334, cooling=0, tap_water=0, pumps=0.12339583333333334, all=0.9158791666666668)
```