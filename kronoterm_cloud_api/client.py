__version__ = "0.1.15"

import logging
from collections import namedtuple
from datetime import datetime

import requests

from kronoterm_cloud_api.kronoterm_enums import (
    APIEndpoint,
    HeatingLoop,
    HeatingLoopMode,
    HeatingLoopStatus,
    HeatPumpOperatingMode,
    WorkingFunction,
)

log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(module)s:%(funcName)s:%(lineno)d - %(message)s"
)


class KronotermCloudApiException(Exception):
    pass


class KronotermCloudApiSetFailedException(KronotermCloudApiException):
    pass


class KronotermCloudApi:
    DEFAULT_HEADERS = {
        "Host": "cloud.kronoterm.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Priority": "u=0, i",
        "Cookie": "",
    }

    def __init__(self, username: str, password: str):
        """Kronoterm heat pump cloud API.

        :param username: kronoterm cloud username
        :param password: kronoterm cloud password
        """
        self.username = username
        self.password = password

        self._base_api_url = "https://cloud.kronoterm.com/jsoncgi.php?"
        self._login_url = "https://cloud.kronoterm.com/?login=1"
        self.headers = None
        self.session_id = None

        # Heat pump information
        self.hp_id: str | None = None
        self.user_level: str | None = None
        self.location_name: str | None = None
        self.loop_names: str | None = None  # CircleNames
        self.active_errors_count: str | None = None

    def login(self):
        """Log in to cloud."""

        login_data = {"username": self.username, "password": self.password}
        self.headers = self.DEFAULT_HEADERS.copy()
        login_response = requests.post(self._login_url, data=login_data, headers=self.headers)
        log.info(login_response.cookies)
        log.info(login_response.status_code)
        if (reason := login_response.cookies.get("AuthReason", None)) is not None:
            log.error("Login failed '%s'", reason)
            raise KronotermCloudApiException("Login failed '%s'", reason)
        self.session_id = login_response.cookies["PHPSESSID"]
        self.headers["Cookie"] = f"PHPSESSID={self.session_id}"
        log.info("Logged in and session cookie set.")

    def get_raw(self, url: str, **kwargs):
        """GET response from given url API endpoint.

        :param url: url of the request
        :param kwargs: any other arguments that will be passed to requests.get()
        :return: response
        """
        url = self._base_api_url + url
        log.info("GET: '%s' [headers='%s', kwargs='%s']", url, self.headers, kwargs)
        response = requests.get(url, headers=self.headers, **kwargs)
        log.info("GET RESP: '%s'", response.text)
        return response

    def post_raw(self, url, **kwargs):
        """POST response from given url API endpoint.

        :param url: url of the request
        :param kwargs: any other arguments that will be passed to requests.post()
        :return: response
        """
        if kwargs.get("headers", False):
            headers = kwargs.get("headers")
            kwargs.pop("headers")
        else:
            headers = self.headers
        url = self._base_api_url + url
        log.info("POST: '%s' [headers='%s', kwargs='%s']", url, headers, kwargs)
        response = requests.post(url, headers=headers, **kwargs)
        log.info("POST RESP: '%s'", response.text)
        return response

    def update_heat_pump_basic_information(self):
        """Update heat pump information from INITIAL load data."""

        data = self.get_initial_data()
        self.hp_id = data.get("hp_id")
        self.user_level = data.get("user_level")
        self.location_name = data.get("Location")
        self.loop_names = data.get("CircleNames")
        self.active_errors_count = int(data.get("ActiveErrorsCnt"))

    def get_initial_data(self) -> dict:
        """Get initial data.

        :return: initial data
        """
        data = self.get_raw(APIEndpoint.INITIAL.value).json()
        return data

    def get_basic_data(self) -> dict:
        """Get basic view data.

        :return: basic view data
        """
        data = self.get_raw(APIEndpoint.BASIC.value).json()
        return data

    def get_system_review_data(self) -> dict:
        """Get system review view data.

        :return: system review data
        """
        data = self.get_raw(APIEndpoint.SYSTEM_REVIEW.value).json()
        return data

    def get_heating_loop_data(self, loop: HeatingLoop) -> dict:
        """Get heating loop view data. Supports:
        - HEATING_LOOP_1
        - HEATING_LOOP_2
        - TAP_WATER

        :return: heating loop data
        """
        match loop:
            case HeatingLoop.HEATING_LOOP_1:
                loop_url = APIEndpoint.HEATING_LOOP_1.value
            case HeatingLoop.HEATING_LOOP_2:
                loop_url = APIEndpoint.HEATING_LOOP_2.value
            case HeatingLoop.TAP_WATER:
                loop_url = APIEndpoint.TAP_WATER.value
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        data = self.get_raw(loop_url).json()
        return data

    def get_alarms_data(self) -> dict:
        """Get alarm view data.

        :return: alarm data
        """
        data = self.get_raw(APIEndpoint.ALARMS.value).json()
        return data

    def get_alarms_data_only(self, alarms_data: dict | None = None) -> dict:
        """Get only AlarmsData (list of alarms) part of the alarm response.

        :param alarms_data: if supplied it will be parsed for AlarmsData otherwise make API request
        :return: list of alarms
        """
        if alarms_data is not None:
            return alarms_data.get("AlarmsData")
        else:
            return self.get_alarms_data().get("AlarmsData")

    def get_theoretical_use_data(self) -> dict:
        """Get theoretical use view data. As displayed in 'Theoretical use histogram'.

        :return: theoretical use data
        """
        url = "TopPage=4&Subpage=4&Action=4"
        # TODO: research dValues[]!!!

        day_of_year = datetime.now().timetuple().tm_yday
        year = datetime.now().timetuple().tm_year
        data = {
            "year": str(year),
            "d1": str(day_of_year),  # day of the year
            "d2": "0",  # hour
            "type": "day",  # # year, month, hour, week, day, hour
            "aValues[]": "17",  # # data to graph
            "dValues[]": ["90", "0", "91", "92", "1", "2", "24", "71"],  # # data to graph
        }
        data = self.post_raw(url, data=data, headers=self.headers).json()
        return data

    def get_outside_temperature(self) -> float:
        """Get current outside temperature.

        :return: outside temperature in [C]
        """
        data = self.get_basic_data()["TemperaturesAndConfig"]["outside_temp"]
        return float(data)

    def get_working_function(self) -> WorkingFunction:
        """Get currently set HP working function

        :return: WorkingFunction Enum
        """
        data = self.get_basic_data()["TemperaturesAndConfig"]["working_function"]
        return WorkingFunction(data)

    def get_room_temp(self) -> float:
        """Get current room temperature.

        :return: room temperature in [C]
        """
        # TODO: This could probably be different if kontrol thermostat is connected to different heating loop?
        room_temp = self.get_basic_data()["TemperaturesAndConfig"]["heating_circle_2_temp"]
        return float(room_temp)

    def get_reservoir_temp(self) -> float:
        """Get current reservoir temperature.

        :return: reservoir temperature in [C]
        """
        reservoir_temp = self.get_basic_data()["TemperaturesAndConfig"]["reservoir_temp"]
        return float(reservoir_temp)

    def get_outlet_temp(self) -> float:
        """Get current HP outlet temperature.

        :return: HP outlet temperature in [C]
        """
        dv_temp = self.get_system_review_data()["CurrentFunctionData"][0]["dv_temp"]
        return float(dv_temp)

    def get_sanitary_water_temp(self) -> float:
        """Get current sanitary water temperature.

        :return: sanitary water temperature in [C]
        """
        dv_temp = self.get_basic_data()["TemperaturesAndConfig"]["tap_water_temp"]
        return float(dv_temp)

    def get_heating_loop_target_temperature(self, loop: HeatingLoop) -> float:
        """Get currently set heating loop target temperature.

        :return: currently set heating loop target temperature in [C]
        """
        set_temp = self.get_heating_loop_data(loop)["HeatingCircleData"]["circle_temp"]
        return float(set_temp)

    def get_heating_loop_status(self, loop: HeatingLoop) -> HeatingLoopStatus:
        """Get HP working status.
           - ECO
           - NORMAL
           - COMFORT
           - OFF
           - AUTO

        :return: HP working status
        """
        status = self.get_heating_loop_data(loop)["HeatingCircleData"]["circle_status"]
        return HeatingLoopStatus(status)

    def get_heating_loop_mode(self, loop: HeatingLoop) -> HeatingLoopMode:
        """Get the mode of heating loop:
           - ON
           - OFF
           - AUTO

        :param loop: for which loop to get mode
        :return mode: mode of the loop
        """
        mode = self.get_heating_loop_data(loop)["HeatingCircleData"]["circle_mode"]
        return HeatingLoopMode(mode)

    def get_heat_pump_operating_mode(self) -> HeatPumpOperatingMode:
        """Get the mode of heating loop:
           - COMFORT
           - AUTO
           - ECO

        :return mode: mode of the heat pumo
        """
        mode = self.get_basic_data()["TemperaturesAndConfig"]["main_mode"]
        return HeatPumpOperatingMode(mode)

    def set_heating_loop_mode(self, loop: HeatingLoop, mode: HeatingLoopMode) -> bool:
        """Set the mode of heating loop:
           - ON
           - OFF
           - AUTO

        :param loop: for which loop to set mode
        :param mode: mode of the loop
        """
        match loop:
            case HeatingLoop.HEATING_LOOP_1:
                loop_url = APIEndpoint.HEATING_LOOP_1_SET.value
                page = 5
            case HeatingLoop.HEATING_LOOP_2:
                loop_url = APIEndpoint.HEATING_LOOP_2_SET.value
                page = 6
            case HeatingLoop.TAP_WATER:
                loop_url = APIEndpoint.TAP_WATER_SET.value
                page = 9
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        request_data = {"param_name": "circle_status", "param_value": mode.value, "page": page}
        response = self.post_raw(loop_url, data=request_data, headers=self.headers).json()
        return response.get("result", False) == "success"

    def set_heat_pump_operating_mode(self, mode: HeatPumpOperatingMode):
        """Set the heat pump operating mode:
           - COMFORT
           - AUTO
           - ECO

        :param mode: mode of the heat pump
        """
        request_data = {"param_name": "main_mode", "param_value": mode.value, "page": -1}
        response = self.post_raw(APIEndpoint.ADVANCED_SETTINGS.value, data=request_data, headers=self.headers).json()
        log.info(response)
        return response.get("result", False) == "success"

    def set_heating_loop_target_temperature(self, loop: HeatingLoop, temperature: int | float) -> bool:
        """Set heating loop temperature.

        :param loop: for which loop to set temperature
        :param temperature: temperature to set
        """
        match loop:
            case HeatingLoop.HEATING_LOOP_1:
                loop_url = APIEndpoint.HEATING_LOOP_1_SET.value
                page = 5
            case HeatingLoop.HEATING_LOOP_2:
                loop_url = APIEndpoint.HEATING_LOOP_2_SET.value
                page = 6
            case HeatingLoop.TAP_WATER:
                loop_url = APIEndpoint.TAP_WATER_SET.value
                page = 9
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        request_data = {"param_name": "circle_temp", "param_value": temperature, "page": page}
        response = self.post_raw(loop_url, data=request_data, headers=self.headers).json()
        return response.get("result", False) == "success"

    def get_theoretical_power_consumption(self):
        """Get theoretically calculated power consumption (calculated by HP and/or cloud).

        :return: named tuple with latest daily power consumption in [kWh]
        """
        data = self.get_theoretical_use_data()

        heating_consumption = data["trend_consumption"]["CompHeating"][-1]
        cooling_consumption = data["trend_consumption"]["CompActiveCooling"][-1]
        tap_water_consumption = data["trend_consumption"]["CompTapWater"][-1]
        pumps_consumption = data["trend_consumption"]["CPLoops"][-1]
        all_consumption = heating_consumption + cooling_consumption + tap_water_consumption + pumps_consumption

        HPConsumption = namedtuple("HPConsumption", ["heating", "cooling", "tap_water", "pumps", "all"])
        return HPConsumption(
            heating=heating_consumption,
            cooling=cooling_consumption,
            tap_water=tap_water_consumption,
            pumps=pumps_consumption,
            all=all_consumption,
        )


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    hp_api = KronotermCloudApi(
        username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD")
    )
    hp_api.login()
    hp_api.update_heat_pump_basic_information()

    for api_return in [
        hp_api.hp_id,
        hp_api.user_level,
        hp_api.location_name,
        hp_api.loop_names,
        hp_api.active_errors_count,
        "-" * 25,
        hp_api.get_initial_data(),
        hp_api.get_basic_data(),
        hp_api.get_system_review_data(),
        hp_api.get_theoretical_power_consumption(),
        "-" * 25,
        hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_1),
        hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_2),
        hp_api.get_heating_loop_data(HeatingLoop.TAP_WATER),
        hp_api.get_heating_loop_mode(HeatingLoop.HEATING_LOOP_1),
        hp_api.get_heating_loop_mode(HeatingLoop.HEATING_LOOP_2),
        hp_api.get_heating_loop_mode(HeatingLoop.TAP_WATER),
        "-" * 25,
        hp_api.get_alarms_data(),
        hp_api.get_heat_pump_operating_mode(),
        # "-" * 25,
        # hp_api.set_heating_loop_mode(HeatingLoop.HEATING_LOOP_1, HeatingLoopMode.AUTO),
        # hp_api.set_heating_loop_mode(HeatingLoop.HEATING_LOOP_2, HeatingLoopMode.AUTO),
        # hp_api.set_heating_loop_mode(HeatingLoop.TAP_WATER, HeatingLoopMode.AUTO),
        # hp_api.set_heat_pump_operating_mode(HeatPumpOperatingMode.AUTO),
    ]:
        print(api_return)

    system_review_data = hp_api.get_system_review_data()
    heat_pump_operating_mode = HeatPumpOperatingMode(system_review_data["TemperaturesAndConfig"]["main_mode"])
    print(heat_pump_operating_mode)
