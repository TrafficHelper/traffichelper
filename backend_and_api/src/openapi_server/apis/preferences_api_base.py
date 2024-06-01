# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.preferences import Preferences


class BasePreferencesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePreferencesApi.subclasses = BasePreferencesApi.subclasses + (cls,)

    def set_preferences(
        self,
        preferences: Preferences,
    ) -> str:
        """Provisioning user preferences"""
        ...
