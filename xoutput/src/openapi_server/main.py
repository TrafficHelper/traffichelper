# coding: utf-8

"""
    Traffic Wise

    This is the API for traffic wise based on OpenAPI 3.0 specification..

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.points_api import router as PointsApiRouter
from openapi_server.apis.preferences_api import router as PreferencesApiRouter
from openapi_server.apis.routes_api import router as RoutesApiRouter

app = FastAPI(
    title="Traffic Wise",
    description="This is the API for traffic wise based on OpenAPI 3.0 specification..",
    version="1.0",
)

app.include_router(PointsApiRouter)
app.include_router(PreferencesApiRouter)
app.include_router(RoutesApiRouter)
