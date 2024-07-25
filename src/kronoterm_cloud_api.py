import logging
from datetime import datetime
from pprint import pprint

import requests
from cachetools import TTLCache, cached
from hp_enums import APIEndpoint, TimelineGraphRequestData, WorkingFunction, ConsumptionHistogramData

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)4s:%(funcName)20s()]\t%(message)s",
    level=logging.DEBUG,
)


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


class KronotermCloudApi:
    def __init__(self, username: str, password: str):
        """Kronoterm heat pump cloud API.

        :param username: kronoterm cloud username
        :param password: kronoterm cloud password
        """
        self.username = username
        self.password = password

        self._base_api_url = "https://cloud.kronoterm.com/jsoncgi.php?"
        self._login_url = "https://cloud.kronoterm.com/?login=1"
        self.headers = DEFAULT_HEADERS.copy()
        self.session_id = None

    def login(self):
        """Log in to cloud."""

        login_data = {"username": self.username, "password": self.password}
        login_response = requests.post(self._login_url, data=login_data, headers=self.headers)
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
        log.debug("GET: '%s'", url)
        response = requests.get(url, headers=self.headers, **kwargs)
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
        log.debug("POST: '%s'", url)
        response = requests.post(url, headers=headers, **kwargs)
        return response

    @cached(cache=TTLCache(maxsize=512, ttl=30))
    def get_system_review(self) -> dict:
        """Get system review data.

        :return: system review data
        """
        data = self.get_raw(APIEndpoint.SYSTEM_REVIEW.value).json()
        return data

    @cached(cache=TTLCache(maxsize=512, ttl=30))
    def get_circle_2(self) -> dict:
        """Get circle 2 data.

        :return: circle 2 data
        """
        data = self.get_raw(APIEndpoint.HEATING_LOOP_2.value).json()
        log.debug(data)
        return data

    def get_outside_temperature(self) -> float:
        """Get current outside temperature.

        :return: outside temperature in [C]
        """
        data = self.get_system_review()["TemperaturesAndConfig"]["outside_temp"]
        return float(data)

    def get_working_function(self) -> WorkingFunction:
        """Get currently set HP working function

        :return: WorkingFunction Enum
        """
        data = self.get_system_review()["TemperaturesAndConfig"]["working_function"]
        return WorkingFunction(data)

    def get_room_temp(self) -> float:
        """Get current room temperature.

        :return: room temperature in [C]
        """
        room_temp = self.get_system_review()["TemperaturesAndConfig"]["heating_circle_2_temp"]
        return float(room_temp)

    def get_reservoir_temp(self) -> float:
        """Get current reservoir temperature.

        :return: reservoir temperature in [C]
        """
        reservoir_temp = self.get_system_review()["TemperaturesAndConfig"]["reservoir_temp"]
        return float(reservoir_temp)

    def get_outlet_temp(self) -> float:
        """Get current HP outlet temperature.

        :return: HP outlet temperature in [C]
        """
        dv_temp = self.get_system_review()["CurrentFunctionData"][0]["dv_temp"]
        return float(dv_temp)

    def get_set_convector_temp(self) -> float:
        """Get currently set convector (room) temperature.

        :return: currently set convector temperature in [C]
        """
        set_temp = self.get_circle_2()["HeatingCircleData"]["circle_temp"]
        return float(set_temp)

    def get_working_status(self) -> bool:
        """Get HP working status.

        :return: HP working status
        """
        status = self.get_circle_2()["HeatingCircleData"]["circle_status"]
        return bool(int(status))

    def get_external_unit_power(self):
        """
        data = {"year": "2024",
                "d1": "195",     # day of the year
                "d2": "21",      # hour ... or not, depending on type
                "type": "hour",  # year, month, hour, week, day, hour
                "aValues[]": "29"}  # analog data to graph

        :return: Current power in [A]
        """
        # research aValues[]!!!

        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        hour = today.hour

        request_data = {
            "year": today.year,
            "d1": day_of_year,
            "d2": hour,
            "type": "hour",
            "aValues[]": TimelineGraphRequestData.ELECTRIC_CONSUMPTION.value,
        }
        response = self.post_raw(APIEndpoint.TIMELINE_GRAPH.value, data=request_data, headers=self.headers).json()
        log.info("today: %s; ", today)
        log.info("request_data: %s", request_data)
        log.info("response: %s", response)

        self.verify_graph_timeseries(response, today)
        power = response["trend_data"]["V29"][-1]
        log.info("power: %s W", power)
        return power

    def get_power_consumption(self) -> float:
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday

        request_data = {
            "year": today.year,
            "d1": day_of_year,
            "d2": 0,
            "type": "day",
            "aValues[]": 17,
            "dValues[]": [91]
        }
        # 91 ...TapWaterLowTariffPerc
        response = self.post_raw(APIEndpoint.CONSUMPTION_HISTOGRAM.value, data=request_data, headers=self.headers).json()
        log.info("today: %s; ", today)
        log.info("request_data: %s", request_data)
        log.info("response: %s", response)
        pprint(response["trend_consumption"]["TapWaterLowTariffPerc"])
        # pprint(response["trend_consumption"]["TapWaterHighTariffPerc"])
        # self.verify_graph_timeseries(response, today)

    @staticmethod
    def verify_graph_timeseries(timeline_graph_response: dict, today: datetime) -> bool:
        """Verify if graph timeseries data is valid by checking
         last timestamp against current time.

        :param timeline_graph_response: response from TIMELINE_GRAPH API endpoint
        :param today: current datetime
        :return: is graph timeseries valid
        """
        day_of_year = today.timetuple().tm_yday
        try:
            raw_seconds = timeline_graph_response["trend_data"]["x"][-1]
        except IndexError as err:
            log.error(err)
            return False
        minutes, seconds = divmod(raw_seconds, 60)
        power_datetime = datetime.strptime(
            f"{today.year} {day_of_year} {today.hour}:{minutes}:{seconds}",
            "%Y %j %H:%M:%S",
        )
        log.info("power_datetime: %s", power_datetime)
        t_d = today - power_datetime
        log.info("t_d.seconds: %s", t_d.seconds)
        if t_d.seconds > 120:
            log.warning(
                "Last power reading is older than 2 minutes. Power reading time '%s'; raw_seconds: %s",
                power_datetime,
                raw_seconds,
            )
            return False
        return True


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    hp_api = KronotermCloudApi(
        username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD")
    )
    hp_api.login()

    Pex = hp_api.get_external_unit_power()
    print(Pex)

    print(hp_api.get_working_function())
    print(hp_api.get_reservoir_temp())
    print(hp_api.get_room_temp())
    print(hp_api.get_circle_2())
    print(hp_api.get_outside_temperature())

    print(hp_api.get_power_consumption())
