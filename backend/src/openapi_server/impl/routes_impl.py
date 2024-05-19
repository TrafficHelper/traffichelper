import json
from typing import List

from backend.Code.Interfaces import interfacer
from openapi_server.apis.routes_api_base import BaseRoutesApi
from openapi_server.models.safe_routes import SafeRoutes
from openapi_server.models.safe_routes_resp import SafeRoutesResp


class RouteImpl(BaseRoutesApi):
    def get_safe_route(self, safe_routes: SafeRoutes) -> List[SafeRoutesResp]:
        safe_rt = safe_routes.to_dict()
        result = interfacer.accept_routing(safe_rt)
        # The results are now a list of quadruples, convert it to a list of dicts for each variable
        query_tbl = [{"routes":[str(coord) for coord in route[0]], "risk":route[1], "traveltime":route[2], "distance":route[3]} for route in result]
        queries = []
        for instance in query_tbl:
            queries += [SafeRoutesResp.from_json(json.dumps(instance))]
        return queries
        # jstr = json.dumps(query_tbl) # The JSON Query
        # print(jstr)
        #
        # # jstr = """ {
        # #     "routes": [
        # #         $result
        # #
        # # """
        # #
        # # jstr = """ {
        # #     "routes": [
        # #         "sheldrake drive",
        # #         "Hunt club road",
        # #         "Viewmount Road"
        # #     ],
        # #     "risk": 0.5,
        # #     "traveltime": 564434,
        # #     "distance": 377
        # #
        # # } """
        #
        # sr = SafeRoutesResp.from_json(jstr)
        # print(sr)
        # return sr
