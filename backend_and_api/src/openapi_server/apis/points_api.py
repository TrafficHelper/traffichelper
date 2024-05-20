# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from backend_and_api.src.openapi_server.apis.points_api_base import BasePointsApi
import backend_and_api.src.openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from backend_and_api.src.openapi_server.models.extra_models import TokenModel  # noqa: F401
from backend_and_api.src.openapi_server.models.coords import Coords


router = APIRouter()

ns_pkg = backend_and_api.src.openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/addresses",
    responses={
        200: {"model": str, "description": "All good"},
    },
    tags=["Points"],
    response_model_by_alias=True,
)
async def get_address_from_lat_long(
    latitude: str = Query(None, description="", alias="latitude"),
    longitude: str = Query(None, description="", alias="longitude"),
) -> str:
    """get address in different format"""
    return BasePointsApi.subclasses[0]().get_address_from_lat_long(latitude, longitude)


@router.get(
    "/latlong",
    responses={
        200: {"model": Coords, "description": "All good"},
    },
    tags=["Points"],
    response_model_by_alias=True,
)
async def get_lat_long_from_address(
    address: str = Query(None, description="", alias="address"),
) -> Coords:
    """get Latitude and Longitude from backend.address"""
    return BasePointsApi.subclasses[0]().get_lat_long_from_address(address)
