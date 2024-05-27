import datetime
import itertools
import osmnx

from backend.Constants import constants
from backend.Code.mutation import Mutation
from backend.Code.user import User


class Utils:

    """
    This class serves as the interface for all user-permitted actions. It is also a major utility class for application.
    Each utility class consists of a central network, a Graph object ostensibly representing traffic network considered
    """

    def __init__(self, user:User):
        self.user = user

    def apply(self, actions:[(Mutation, bool)]):
        """
        Modifies this current network after the modifications have been applied to it
        :param actions: The sequence of actions, a Modification, to apply to the network
        :return: A Network after the actions have been applied, refactored for changes
        """
        if not self.user.is_admin:
            raise PermissionError('Insufficient privileges to make action!')
        for act in actions:
            act[0].apply(act[1])

    def optimal_paths(self, departure:datetime.datetime, start, finish, amount:int = 1):
        """
        Returns all optimal paths given the list of preferences, departure time, start and finish nodes, and number
        These optimal paths are in a dictionary, associating each path (represented by its identity, sequence of nodes)
        - Total path accident risk (for the accident tolerance stipulated in the preferences, any accident here; but this may be specialized from the CLI)
        - Total path time, elapsed distance
        - Total path distance
        :param departure:
        :param start: The beginning coordinates (lat, long)
        :param finish: The end coordinate (lat, long)
        :param amount:
        :return:
        """
        # TODO Return even better route safe algo
        # The network should already have been modified to account for the user's presence, drawing on the user's network in the first place
        # Each vehicle's accident risk increases proportional to its type
        ini = start if isinstance(start, int) else osmnx.nearest_nodes(self.user.curr_network, start[1], start[0])
        end = finish if isinstance(finish, int) else osmnx.nearest_nodes(self.user.curr_network, finish[1], finish[0])
        best_paths = [*osmnx.k_shortest_paths(self.user.curr_network, ini, end, amount, weight="cost")] # Replace with weight="length" as backup
        results:{[int]:(float, float, float)} = {} # List of the best paths against accident risk,
        for path in best_paths:
            route_safe = 1.0
            route_time = 0.0
            route_dist = 0.0
            for nde, nxt in zip(path, path[1:]):
                properties = self.user.curr_network.get_edge_data(nde, nxt)[0]
                edge_risk = float(properties['risk'])
                route_safe *= abs(1-edge_risk) # Here, we multiply for probability of particular risk not occurring
                print(route_safe)
                edge_time = properties['travel_time']
                route_time += edge_time
                edge_dist = properties['length']
                route_dist += edge_dist
            tst = lambda chance: chance/10 if 0.01 <= chance <= 0.1 else chance/100 if 0.1 <= chance <= 1 else chance
            results[tuple(path)] = tst(route_safe), route_time, route_dist # Chance of accident, time and distance
        return results

    def print_paths(self, optimal_paths:{}):
        """
        :param optimal_paths: The dict of optimal paths and another parameter, most likely from the optimal_paths method
        :return: Convenience method to overlay printed optimal paths on user's graph network
        """
        routes = [list(e) for e in optimal_paths.keys()]
        if len(routes) == 1:
            osmnx.plot_graph_route(self.user.curr_network, routes[0])
        else:
            osmnx.plot_graph_routes(self.user.curr_network, routes)

    def best_predictions(self, budget:int = constants.NORMAL_BUDGET, amount:int = 1) -> [[Mutation]]:
        # TODO Refactor, has been moved to frontend API
        """
        Returns a sequence of Mutation which are logically consistent and minimize the cost metric given the user's preference of such a cost metric, within budget
        :param budget: The given budget, in dollars
        :param amount: The given number of mutation
        :return: The required number of Mutation which are within the given budget and which minimize the user's cost metric
        """
        if not self.user.is_admin:
            raise PermissionError('Accessor does not have sufficient privileges!')

    def paths_names(self, paths):#{[int]:(float, float, float)}):
        """
        :param paths: The list of paths consisting of a sequence of a sequence of integer nodeIDs/OSMids
        :return: Return an identical new path sequence with each term converted to a road name
        """

        edges_names = self.user.curr_network.edges
        nodes_names = self.user.curr_network.nodes
        result = [] # Note: The returned result is a LIST and not a DICT
        for route in paths:
            road_names = [edges_names[(u, v, 0)]["name"] if (u, v, 0) in edges_names and "name" in edges_names[(u, v, 0)] else "_" for u, v in zip(route, route[1:])]
            # Remove all successive duplicate road names in order-preserving fashion, while preserving the risk, time and dist
            result += [([[rn[0] for rn in itertools.groupby(road_names)]], paths[route][0], paths[route][1], paths[route][2])]
        return result

    def paths_coordinates(self, paths):#{[int]:(float, float, float)}):
        """
        :param paths: The list of paths, each one consisting of a sequence of nodeID/OSMid nodes
        :return: Returns a new path sequence with each node replaced by a coordinate
        """
        point_coords = self.user.curr_network.nodes
        # Convert dict of paths to list of paths with new information and previously-placed identical information
        return [([(point_coords[node]['y'], point_coords[node]['x']) for node in route], paths[route][0], paths[route][1], paths[route][2]) for route in paths]

# if __name__ == '__main__':
#     start = osmnx.geocode('4100 Russell Road, Ottawa, Canada')
#     end = osmnx.geocode('150 Elgin Street, Canada')
#     me = User()
#     apparatus = Utils(me)
#     traversals = apparatus.optimal_paths(datetime.datetime.now(), start, end)
#
#     # Get coordinates, road names and print optimal paths
#     print(traversals)
#     coordinates = apparatus.paths_coordinates(traversals)
#     print(coordinates)
#     roadnames = apparatus.paths_names(traversals)
#     print(roadnames)
#     # Print the paths directly
#     apparatus.print_paths(traversals)




