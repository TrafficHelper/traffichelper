# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.coords import Coords


class BasePointsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePointsApi.subclasses = BasePointsApi.subclasses + (cls,)
    def get_address_from_lat_long(
        self,
        latitude: str,
        longitude: str,
    ) -> str:
        """get address in different format"""
        ...


    def get_lat_long_from_address(
        self,
        address: str,
    ) -> Coords:
        """get Latitude and Longitude from backend address"""
        ...
