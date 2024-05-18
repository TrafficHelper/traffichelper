import datetime
import itertools

import geopy
import networkx
import osmnx

import constants
from Code.mutation import Mutation
from Code.user import User


class Utils:

    """
    This class serves as the interface for all user-permitted actions. It is also a major utility class for application.
    Each utility class consists of a central network, a Graph object ostensibly representing traffic network considered
    """

    def __init__(self, user:User):
        self.user = user

    def apply(self, actions:[Mutation]):
        """
        Modifies this current network after the modifications have been applied to it
        :param actions: The sequence of actions, a Modification, to apply to the network
        :return: A Network after the actions have been applied, refactored for changes
        """
        if not self.user.is_admin:
            raise PermissionError('Insufficient privileges to make action!')
        for act in actions:
            act.apply(self.user.curr_network, True)

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

        # The network should already have been modified to account for the user's presence, drawing on the user's network in the first place
        # Each vehicle's accident risk increases proportional to its type
        ini = osmnx.nearest_nodes(self.user.curr_network, start[1], start[0])
        end = osmnx.nearest_nodes(self.user.curr_network, finish[1], finish[0])
        best_paths = [*osmnx.k_shortest_paths(self.user.curr_network, ini, end, amount, weight="cost")] # Replace with weight="length" as backup
        results:{[int]:(float, float, float)} = {} # List of the best paths against accident risk,
        for path in best_paths:
            route_safe = 1
            route_time = 0
            route_dist = 0
            for nde, nxt in zip(path, path[1:]):
                properties = self.user.curr_network.get_edge_data(nde, nxt)[0]
                edge_risk = float(properties['risk'])
                route_safe *= (1-edge_risk) # Here, we multiply for probability of particular risk not occurring
                edge_time = properties['travel_time']
                route_time += edge_time
                edge_dist = properties['length']
                route_dist += edge_dist
            results[tuple(path)] = 1 - route_safe, route_time, route_dist # Chance of accident, time and distance
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
        """
        Returns a sequence of Mutation which are logically consistent and minimize the cost metric given the user's preference of such a cost metric, within budget
        :param budget: The given budget, in dollars
        :param amount: The given number of mutation
        :return: The required number of Mutation which are within the given budget and which minimize the user's cost metric
        """
        if not self.user.is_admin:
            raise PermissionError('Accessor does not have sufficient privileges!')

    def beautify(self, paths: [[int]]):
        """
        :param paths: The list of paths represented by OSMnx Node
        :return: Converts each path to a sequence of Addresses ~ Street names, efficiency in bulk
        """
        res = []
        for path in paths:
            edges = [self.user.curr_network[this][foll][0] for this, foll in zip(path, path[1:])]
            road_names = networkx.get_edge_attributes(set(edges), 'name') # Get road names
            road_names = [elem for elem, _group in itertools.groupby(road_names)]
            res += [road_names]
        return res




