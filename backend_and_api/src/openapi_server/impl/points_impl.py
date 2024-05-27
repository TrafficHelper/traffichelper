import geopy.geocoders
import osmnx

from backend.Code.Interfaces import interfacer
from openapi_server.apis.points_api_base import BasePointsApi
from openapi_server.models.coords import Coords

class PointsImpl(BasePointsApi):

    def get_lat_long_from_address(self, address: str) -> Coords:
        """
        Gets the latitude and longitude from str address
        :param address: str, represents address
        :return: Returns the latitude and longitude from address
        """
        print(address)
        interfacer.select_start(address)
        loc = osmnx.geocode(address)
        json_tmp = {'latitude':str(loc[0]), 'longitude':str(loc[1])}
        print(json_tmp)
        coord = Coords.from_dict(json_tmp)
        return coord

    def get_address_from_lat_long(self, latitude: str, longitude: str) -> str:
        """
        Gets the address from chosen latitude and longitude
        :param latitude: The latitude of the locale
        :param longitude: The longitude of the locale
        :return: Selects the lat, long of the locale.
        """
        print(latitude, longitude)
        interfacer.select_start((latitude, longitude)) # Interpret from coord tuple
        return "Default address"
