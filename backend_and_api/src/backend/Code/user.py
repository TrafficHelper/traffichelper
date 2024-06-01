import copy

import networkx
import osmnx

from backend.Code import loader, mutation
from backend.Code.Accident.accident import Accident
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Utils.preferences import Preferences
from backend.Constants import constants

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

        self._preferences = new  # Finally set new preferences
        num_envts = 5.0 # Number of environments
        self.curr_network = copy.deepcopy(self.base_network) # Reset to work with base network, discarding previous changes
        new_accidents = {}
        # elt = self.curr_network.edges
        for u, v, key in self.curr_network.edges:
            accidents:[Accident] = self.curr_network[u][v][key]['accidents']
            # print(accidents)
            # Remove according to user's environment, each environment has rank/total() of all accidents
            accidents = mutation.Mutation.trim(accidents, self.preferences.environment.value/num_envts*self.preferences.metric[0])
            # print(accidents)
            # Then Remove all intolerable accidents
            valid_accidents = accidents # List of new valid accidents on edge
            for elem in accidents:
                if elem in self.preferences.intolerance:
                    valid_accidents.remove(elem)
            new_accidents[(u, v, key)] = valid_accidents
        max_speed = networkx.get_edge_attributes(self.curr_network, 'speed_kph')
        if self.preferences.vehicle in [Vehicle.PEDESTRIAN]:
            max_speed = {edge:constants.PEDESTRIAN_MAX_SPEED for edge in max_speed}
        if self.preferences.vehicle in [Vehicle.BICYCLE]:
            max_speed = {edge:constants.BICYCLE_MAX_SPEED for edge in max_speed}
        networkx.set_edge_attributes(self.curr_network, max_speed, 'speed_kph')
        osmnx.add_edge_travel_times(self.curr_network)

        # Add accidents to recompute them
        networkx.set_edge_attributes(self.curr_network, new_accidents, 'accidents')
        loader.compute_risks(self.curr_network) # Recompute new risks
        loader.compute_costs(self.curr_network, new.metric) # ... Thus recompute new costs


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

# Tester
# if __name__ == '__main__':
#     us = User()
#     print(us.preferences)
#     us.preferences = Preferences(Vehicle.PEDESTRIAN, Environment.ABNORMAL, (0.1, 0.3, 0.6))
#     print(us.preferences)
#
