import os

import pytest
from dotenv import load_dotenv

from kronoterm_cloud_api import KronotermCloudApi

load_dotenv()


@pytest.fixture(scope="session")
def kronoterm_user() -> dict:
    """Get kronoterm cloud username and password as dict.

    :return: username and password as dict
    """
    return {"username": os.getenv("KRONOTERM_CLOUD_USER"), "password": os.getenv("KRONOTERM_CLOUD_PASSWORD")}


@pytest.fixture(scope="module")
def kronoterm_cloud_api(kronoterm_user) -> KronotermCloudApi:
    """Get KronotermCloudApi object. User NOT logged in!

    :return: KronotermCloudApi
    """
    return KronotermCloudApi(username=kronoterm_user["username"], password=kronoterm_user["password"])
