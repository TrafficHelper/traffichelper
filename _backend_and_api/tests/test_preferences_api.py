# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.preferences import Preferences  # noqa: F401


def test_set_preferences(client: TestClient):
    """Test case for set_preferences

    
    """
    preferences = {"vehicletype":"CAR","environment":"NORMAL","path_choices":{"distance":0.14658129,"safety":0.08008282,"time_of_day":0.6027456}}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/prefer",
    #    headers=headers,
    #    json=preferences,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

