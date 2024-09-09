[![ruff](https://github.com/LeskoIam/kronoterm_cloud_api/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_api/actions/workflows/ruff.yml)
# Kronoterm cloud API (unofficial)

API client for controlling Kronoterm heat pumps via their cloud (cloud.kronoterm.com/).

## Installation

1. Install using `pip`
   ```shell
   python -m pip install kronoterm_cloud_api
   ```
2. Enjoy!

## Examples

```python
from kronoterm_cloud_api import KronotermCloudApi
from kronoterm_cloud_api import HeatingLoop, HeatingLoopMode

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
print(hp_api.get_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP))  # Get the mode of heating loop.
# >> HeatingLoopMode.AUTO

print(hp_api.set_heating_loop_target_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP, 24))  # Set heating loop temperature.
# >> True
print(
   hp_api.set_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP, HeatingLoopMode.AUTO))  # Set the mode of heating loop.
# >> True

```