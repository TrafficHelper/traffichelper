from backend.Code.Interfaces import interfacer
from openapi_server.apis.preferences_api_base import BasePreferencesApi
from openapi_server.models.preferences import Preferences


class PreferencesImpl(BasePreferencesApi):

    def set_preferences(self, preferences: Preferences) -> str:
        prefs = preferences.to_dict()
        result = interfacer.accept_preferences(prefs)
        print(interfacer.PATH_METRIC)
        print(interfacer.SELECTED_VEHICLE)
        print(interfacer.SELECTED_ENVIRONMENT)
        return result


