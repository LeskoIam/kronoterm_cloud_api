__version__ = "0.1.3"

import logging

import requests

from kronoterm_enums import APIEndpoint, HeatingLoop, HeatingLoopMode, WorkingFunction

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)4s:%(funcName)20s()]\t%(message)s",
    level=logging.INFO,
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

    def get_system_review_data(self) -> dict:
        """Get system review data.

        :return: system review data
        """
        data = self.get_raw(APIEndpoint.SYSTEM_REVIEW.value).json()
        return data

    def get_heating_loop_data(self, loop: HeatingLoop) -> dict:
        """Get heating loop data.

        :return: heating loop data
        """
        match loop:
            case HeatingLoop.LOW_TEMPERATURE_LOOP:
                loop_url = APIEndpoint.HEATING_LOOP_2.value
            # case HeatingLoop.HIGH_TEMPERATURE_LOOP:
            #     loop_url = APIEndpoint.HEATING_LOOP_1.value
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        data = self.get_raw(loop_url).json()
        return data

    def get_outside_temperature(self) -> float:
        """Get current outside temperature.

        :return: outside temperature in [C]
        """
        data = self.get_system_review_data()["TemperaturesAndConfig"]["outside_temp"]
        return float(data)

    def get_working_function(self) -> WorkingFunction:
        """Get currently set HP working function

        :return: WorkingFunction Enum
        """
        data = self.get_system_review_data()["TemperaturesAndConfig"]["working_function"]
        return WorkingFunction(data)

    def get_room_temp(self) -> float:
        """Get current room temperature.

        :return: room temperature in [C]
        """
        room_temp = self.get_system_review_data()["TemperaturesAndConfig"]["heating_circle_2_temp"]
        return float(room_temp)

    def get_reservoir_temp(self) -> float:
        """Get current reservoir temperature.

        :return: reservoir temperature in [C]
        """
        reservoir_temp = self.get_system_review_data()["TemperaturesAndConfig"]["reservoir_temp"]
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
        dv_temp = self.get_system_review_data()["TemperaturesAndConfig"]["tap_water_temp"]
        return float(dv_temp)

    def get_heating_loop_target_temperature(self, loop: HeatingLoop) -> float:
        """Get currently set convector (room) temperature.

        :return: currently set convector temperature in [C]
        """
        set_temp = self.get_heating_loop_data(loop)["HeatingCircleData"]["circle_temp"]
        return float(set_temp)

    def get_heating_loop_working_status(self, loop: HeatingLoop) -> bool:
        """Get HP working status.

        :return: HP working status
        """
        status = self.get_heating_loop_data(loop)["HeatingCircleData"]["circle_status"]
        return bool(int(status))

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

    def set_heating_loop_mode(self, loop: HeatingLoop, mode: HeatingLoopMode) -> bool:
        """Set the mode of heating loop:
           - ON
           - OFF
           - AUTO

        :param loop: for which loop to set mode
        :param mode: mode of the loop
        """
        match loop:
            case HeatingLoop.LOW_TEMPERATURE_LOOP:
                loop_url = APIEndpoint.SET_HEATING_LOOP_2.value
            # case HeatingLoop.HIGH_TEMPERATURE_LOOP:
            #     loop_url = APIEndpoint.SET_HEATING_LOOP_1.value
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        request_data = {"param_name": "circle_status", "param_value": mode.value, "page": 6}
        response = self.post_raw(loop_url, data=request_data, headers=self.headers).json()
        return response.get("result", False) == "success"

    def set_heating_loop_target_temperature(self, loop: HeatingLoop, temperature: int | float) -> bool:
        """Set heating loop temperature.

        :param loop: for which loop to set temperature
        :param temperature: temperature to set
        """
        match loop:
            case HeatingLoop.LOW_TEMPERATURE_LOOP:
                loop_url = APIEndpoint.SET_HEATING_LOOP_2.value
            # case HeatingLoop.HIGH_TEMPERATURE_LOOP:
            #     loop_url = APIEndpoint.SET_HEATING_LOOP_1.value
            case _:
                raise ValueError(f"Heating loop '{loop.name}' not supported")
        request_data = {"param_name": "circle_temp", "param_value": temperature, "page": 6}
        response = self.post_raw(loop_url, data=request_data, headers=self.headers).json()
        return response.get("result", False) == "success"


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    hp_api = KronotermCloudApi(
        username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD")
    )
    hp_api.login()

    print(hp_api.set_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP, HeatingLoopMode.AUTO))
    print(hp_api.get_working_function())
    print(hp_api.get_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP))
    print(hp_api.set_heating_loop_target_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP, 24))

    print(hp_api.get_reservoir_temp())
    print(hp_api.get_room_temp())
    print(hp_api.get_outside_temperature())
    print(hp_api.get_sanitary_water_temp())
    print(hp_api.get_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP))
    print(hp_api.get_heating_loop_working_status(HeatingLoop.LOW_TEMPERATURE_LOOP))
