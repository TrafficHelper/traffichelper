# coding: utf-8

from fastapi.testclient import TestClient

from backend import SafeRoutes  # noqa: F401
from backend import SafeRoutesResp  # noqa: F401


def test_get_safe_route(client: TestClient):
    """Test case for get_safe_route

    
    """
    safe_routes = {"start_time":"2000-01-23T04:56:07.000+00:00","environment":"Normal","path_choices":{"distance":0.14658129,"safety":0.08008282,"time_of_day":0.6027456},"path_count":2.981066958341591,"coordinates":{"destination_address":"40 Merivale Road, Ottawa","start_address":"8 Sheldrake Drive Kanata"}}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/saferoute",
    #    headers=headers,
    #    json=safe_routes,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

