# coding: utf-8

from fastapi.testclient import TestClient
from backend import Coords  # noqa: F401


def test_get_address_from_lat_long(client: TestClient):
    """Test case for get_address_from_lat_long

    
    """
    params = [("latitude", '45.424721'),     ("longitude", '-75.695000')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/addresses",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_lat_long_from_address(client: TestClient):
    """Test case for get_lat_long_from_address

    
    """
    params = [("address", '8 Sheldrake Drive Kanata')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/latlong",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

