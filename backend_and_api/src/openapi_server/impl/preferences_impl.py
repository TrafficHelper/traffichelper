import osmnx

from backend_and_api.src.backend.Code.Interfaces import interfacer
from backend_and_api.src.openapi_server.apis.preferences_api_base import BasePreferencesApi
from backend_and_api.src.openapi_server.models.preferences import Preferences


class PreferencesImpl(BasePreferencesApi):

    def set_preferences(self, preferences: Preferences) -> str:
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        prefs = preferences.to_dict()
        result = interfacer.accept_preferences(prefs)
        print("helllllllllooooooo")
        return result


