# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from backend_and_api.src.openapi_server.apis.preferences_api_base import BasePreferencesApi
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
from backend_and_api.src.openapi_server.models.preferences import Preferences


router = APIRouter()

ns_pkg = backend_and_api.src.openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/prefer",
    responses={
        200: {"description": "Confirm Preferences are set"},
    },
    tags=["Preferences"],
    response_model_by_alias=True,
)
async def set_preferences(
    preferences: Preferences = Body(None, description="JSON Settings"),
) -> None:
    ...
