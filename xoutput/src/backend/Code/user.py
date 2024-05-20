import copy

import networkx
import osmnx

from backend.Code import loader, mutation
from backend.Code.Accident.accident import Accident
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Utils.preferences import Preferences


class User:

    """
    Represents a (super)user account on the Traffic application
    Created whenever someone creates "new user" on the website and optionally sets it to admin privileges, with a passwd
    Consists of a personalized editable network and a private administrator variable, which can be changed
    Actions are discriminated based on the user and/or admin privileges
    """

    def __init__(self, base_network:networkx.MultiDiGraph = loader.LOADED_TRAFFIC_NETWORK, is_admin:bool = False):
        # Depending on the user's shifting preferences, this base network serves as an anchor for the curr_network
        # Every preference change works on the base network
        self.base_network = base_network
        self._curr_network = self.base_network
        self.is_admin = is_admin
        self._preferences = Preferences() # Default set of preferences

    @property
    def curr_network(self):
        return self._curr_network

    @curr_network.setter
    def curr_network(self, new:networkx.MultiDiGraph):
        self._curr_network = new

    @property
    def preferences(self):
        """
        :return: The user's current preference setting
        """
        return self._preferences

    @preferences.setter
    def preferences(self, new:Preferences):
        """
        Sets the user's preferences to the (new) given network.
        Initially, the network consists of solely the standard traffic network, with all its loaded data
        The network is then slightly modified to account for the user's preferences
        - Vehicles: Only accidents involving a particular type of vehicle are included
        - Cost: The 'cost' parameter is modified as the vector product of the edges
        :param new: The preferences of the user
        :return: Modifies the traffic network based on the user's preferences, for easier computation
        """

        self.curr_network = copy.deepcopy(self.base_network) # Reset to work with base network, discarding previous changes
        new_accidents = {}
        for u, v, key in self.curr_network.edges:
            accidents:[Accident] = self.curr_network[u][v][key]['accidents']

            # Remove according to user's environment, each environment has rank/total() of all accidents
            accidents = mutation.Mutation.trim(accidents, self.preferences.environment.value / 5.0)

            # Account for vehicle: Pedestrians and Bicycles have a considered maximum speed of 30 kmh
            if self.preferences.vehicle in [Vehicle.PEDESTRIAN, Vehicle.BICYCLE]:
                max_speed = networkx.get_edge_attributes(self.curr_network, 'speed_kph')
                max_speed = {edge:30 for edge in max_speed} # Upper limit to 30, but they aren't limited
                # Set edge speed limit and recompute travel time
                networkx.set_edge_attributes(self.curr_network, max_speed, 'speed_kph')
                osmnx.add_edge_travel_times(self.curr_network)

            # Then Remove all intolerable accidents
            valid_accidents = accidents # List of new valid accidents on edge
            for elem in accidents:
                if elem in self.preferences.intolerance:
                    valid_accidents.remove(elem)
            new_accidents[u, v, key] = valid_accidents

        networkx.set_edge_attributes(self.curr_network, new_accidents, 'accidents')
        loader.compute_risks(self.curr_network) # Recompute new risks
        loader.compute_costs(self.curr_network, new.metric) # ... Thus recompute new costs
        self._preferences = new # Finally set new preferences

    def make_admin(self):
        self.is_admin = True

    def reset(self):
        """
        Resets the user's traffic network to the default starting network
        :return:
        """
        self.curr_network = self.base_network

    def __str__(self):
        return 'Admin: '+str(self.is_admin)+'. Preferences: '+str(self.preferences)
