# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from backend_and_api.src.openapi_server.models.safe_routes import SafeRoutes
from backend_and_api.src.openapi_server.models.single_resp import SingleResp


class BaseRoutesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRoutesApi.subclasses = BaseRoutesApi.subclasses + (cls,)
    def get_safe_route(
        self,
        safe_routes: SafeRoutes,
    ) -> List[SingleResp]:
        """Get the routes"""
        ...
