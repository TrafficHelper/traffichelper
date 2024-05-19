import geopy.geocoders
import osmnx

from backend.Code.Interfaces import interfacer
from openapi_server.apis.points_api_base import BasePointsApi


class PointsImpl(BasePointsApi):

    def get_lat_long_from_address(self, address: str) -> (float, float):

        interfacer.select_start(address)
        return interfacer.START_NODE

    def get_address_from_lat_long(
            self,
            latitude: str,
            longitude: str,
    ) -> str:
        return geopy.geocoders.Nominatim(user_agent="").reverse(latitude + ", " + longitude)
