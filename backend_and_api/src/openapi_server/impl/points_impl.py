import geopy.geocoders
import osmnx

from backend.Code.Interfaces import interfacer
from openapi_server.apis.points_api_base import BasePointsApi


class PointsImpl(BasePointsApi):

    def get_lat_long_from_address(self, address: str) -> (float, float):
        """
        Gets the latitude and longitude from str address
        :param address: str, represents address
        :return: Returns the latitude and longitude from address
        """
        interfacer.select_start(address)

    def get_address_from_lat_long(self, latitude: str, longitude: str) -> str:
        """
        Gets the address from chosen latitude and longitude
        :param latitude: The latitude of the locale
        :param longitude: The longitude of the locale
        :return: Selects the lat, long of the locale.
        """
        interfacer.select_start((latitude, longitude)) # Interpret from coord tuple
        return ""