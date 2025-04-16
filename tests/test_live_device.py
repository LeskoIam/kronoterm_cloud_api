import logging
import time

import pytest
from kronoterm_enums import HeatingLoop, HeatingLoopMode

from kronoterm_cloud_api.client import KronotermCloudApiException

log = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def restore_target_temperature(heating_loop, kronoterm_cloud_api):
    # Get the current temperature
    original_temperature = kronoterm_cloud_api.get_heating_loop_target_temperature(heating_loop)
    log.info("Original temperature for loop %s: %s", heating_loop, original_temperature)
    yield original_temperature
    log.info("Restoring target temperature for loop %s: %s", heating_loop, original_temperature)
    kronoterm_cloud_api.set_heating_loop_target_temperature(heating_loop, original_temperature)


@pytest.fixture(scope="function")
def restore_loop_mode(heating_loop: HeatingLoop, kronoterm_cloud_api):
    # Get the current loop mode
    original_mode = kronoterm_cloud_api.get_heating_loop_mode(heating_loop)
    log.info("Original mode for loop %s: %s", heating_loop.name, original_mode.name)
    yield original_mode
    log.info("Restoring mode for loop %s: %s", heating_loop, original_mode)
    kronoterm_cloud_api.set_heating_loop_mode(heating_loop, original_mode)


@pytest.mark.parametrize(
    "heating_loop",
    [HeatingLoop.HEATING_LOOP_1, HeatingLoop.HEATING_LOOP_2, HeatingLoop.TAP_WATER],
    ids=["Loop 1", "Loop 2", "Tap Water"],
)
def test_set_loop_target_temperature(heating_loop, kronoterm_cloud_api, restore_target_temperature):
    """
    GIVEN user with valid credentials
    WHEN the user tries to set loop temperature to current temperature -0.3 degree
    THEN set loop temperature must succeed (no exception raised),
      AND the temperature must be set to current temperature -0.3 degree
    """
    original_temperature = restore_target_temperature

    # Set the target temperature to current temperature -0.3 degree
    try:
        log.info(kronoterm_cloud_api.set_heating_loop_target_temperature(heating_loop, original_temperature - 0.3))
    except KronotermCloudApiException as e:
        pytest.fail(e)
    time.sleep(15)
    assert kronoterm_cloud_api.get_heating_loop_target_temperature(heating_loop) == original_temperature - 0.3


@pytest.mark.parametrize(
    "heating_loop",
    [HeatingLoop.HEATING_LOOP_1, HeatingLoop.HEATING_LOOP_2, HeatingLoop.TAP_WATER],
    ids=["Loop 1", "Loop 2", "Tap Water"],
)
@pytest.mark.parametrize(
    "loop_mode", [HeatingLoopMode.OFF, HeatingLoopMode.ON, HeatingLoopMode.AUTO], ids=["OFF", "ON", "AUTO"]
)
def test_set_loop_mode(kronoterm_cloud_api, heating_loop, loop_mode, restore_loop_mode):
    """
    GIVEN user with valid credentials
    WHEN the user tries to set loop mode to <loop_mode>
    THEN set loop mode must succeed (no exception raised),
      AND the mode must be set to <loop_mode>

    Examples:
      | loop_mode |
      | OFF       |
      | ON        |
      | AUTO      |
    """
    # Set the target temperature to current temperature -0.3 degree
    try:
        log.info(kronoterm_cloud_api.set_heating_loop_mode(HeatingLoop.HEATING_LOOP_1, loop_mode))
    except KronotermCloudApiException as exc:
        pytest.fail(exc)
    time.sleep(15)
    assert kronoterm_cloud_api.get_heating_loop_mode(HeatingLoop.HEATING_LOOP_1) == loop_mode
