# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.routes_api_base import BaseRoutesApi
import openapi_server.impl

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

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.safe_routes import SafeRoutes
from openapi_server.models.single_resp import SingleResp


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/saferoute",
    responses={
        200: {"model": List[SingleResp], "description": "Successful return of routes"},
    },
    tags=["Routes"],
    response_model_by_alias=True,
)
async def get_safe_route(
    safe_routes: SafeRoutes = Body(None, description="JSON Settings"),
) -> List[SingleResp]:
    """Get the routes"""
    return BaseRoutesApi.subclasses[0]().get_safe_route(safe_routes)
