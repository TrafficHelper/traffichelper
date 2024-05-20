import json
from typing import List

from backend_and_api.src.backend.Code.Interfaces import interfacer
from backend_and_api.src.openapi_server.apis.routes_api_base import BaseRoutesApi
from backend_and_api.src.openapi_server.models.safe_routes import SafeRoutes
from backend_and_api.src.openapi_server.models.safe_routes_resp import SafeRoutesResp


class RouteImpl(BaseRoutesApi):
    def get_safe_route(self, safe_routes: SafeRoutes) -> List[SafeRoutesResp]:
        safe_rt = safe_routes.to_dict() # Consist of addresses
        result = interfacer.accept_routing(safe_rt)
        # The results are now a list of quadruples, convert it to a list of dicts for each variable
        query_tbl = [{"routes":[str(coord) for coord in route[0]], "risk":route[1], "traveltime":route[2], "distance":route[3]} for route in result]
        return [SafeRoutesResp.from_json(json.dumps(instance)) for instance in query_tbl] # Will return a LIST of quadruples, with the first element a list of coordinates
