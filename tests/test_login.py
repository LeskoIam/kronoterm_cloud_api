import pytest

from kronoterm_cloud_api.client import KronotermCloudApi, KronotermCloudApiException


@pytest.mark.live
def test_login_success(kronoterm_user: dict):
    """
    GIVEN user with valid credentials
    WHEN user tries to log-in
    THEN log-in must succeed (no exception raised)
    """
    kronoterm_cloud_api = KronotermCloudApi(**kronoterm_user)
    try:
        kronoterm_cloud_api.login()
    except KronotermCloudApiException as e:
        pytest.fail(e)


@pytest.mark.live
def test_login_failed(kronoterm_user: dict):
    """
    GIVEN user with invalid credentials
    WHEN user tries to log-in
    THEN log-in must fail with KronotermCloudApiException exception
    """
    kronoterm_cloud_api = KronotermCloudApi(username="TestUserNonExisting", password=kronoterm_user["password"])
    with pytest.raises(KronotermCloudApiException, match="Login failed"):
        kronoterm_cloud_api.login()
