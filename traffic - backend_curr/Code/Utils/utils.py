from Code.DS.Mutation.component import Intersection
from Code.DS.Mutation.modification import Modification
from Code.DS.Mutation.path import Path
from Code.DS.Structural.graph import Node, Edge, Graph, Tracker
from Code.DS.Temporal.time import Time
from Code.Utils.preferences import Preferences


class Utils:

    """
    This class serves as the interface for all user-permitted actions. It is also a major utility class for the application.\n
    Each utility class consists of a central network, a Graph object ostensibly representing the traffic network considered
    """

    def __init__(self, network:Graph):
        self.network = network
        self._finished = {e:False for e in self.network.nodes}

    @property
    def finished(self):
        return self._finished




    def apply(self, actions:Modification):

        """
        Applies the sequence of Modifications to the subject Graph.
        It will directly mutate the Graph rather than on a copy of it.
        To provide a potentiality of the Graph upon mutation
        - Use the Graph.deepcopy() method to copy the Graph
        - Create a Utils(deepcopy) object of the Graph
        - Apply the method on the new created object
        :param actions: The sequence of Modifications are to be applied on the Graph
        :return: A Graph with the sequence of actions applied to it.
        """


    def optimal(self, preferences:Preferences, departure:Time, start:Node, finish:Node, number:int = 1):
        """
        Returns the given number of optimal paths on the network for the user given their Preferences, Time departure, start and end Node \n
        Each of the paths is one of the given number of optimal paths along the network.

        If the user wants to avoid particular edges, then they can re-instantiate this object (referring to a copy of the Graph), crop all avoided Edge, and recall this function

        :param preferences: The user's Preference (Vehicle, Accident,
        :param departure: The time of starting for the journey
        :param start: The starting Node
        :param finish: The finishing Node
        :param number: The number of best paths to be returned
        :return: The given number of optimal paths obeying the parameters
        """

        start_pt = Intersection(start, preferences, departure)
        self.bfs(start_pt)
        minimal = finish.tracker.optimal # The minimal costs and their respective (Node, Edge) pairs where they came from
        return minimal

    def bfs(self, current:Intersection):
        current.node.tracker.count+=1
        if current.node.tracker.count == len(self.network.nodes)**2: # Stop iterating
            self.finished[current.node] = True # Done iterating, don't call anymore
            return current.node.tracker.optimal
        others:[(Edge, Node, float)] = current.domain() # List of Edge-Node pairs, along with costs that can be reached
        for step in others:
            subject = step[2] # Where to reach
            if not self.finished[subject]:
                optimal = self.bfs(subject) # A list of the minimal-length path tracker
                optimal = [step[3] + i for i in optimal]
                current.node.tracker.update(optimal) # Update with new lowest costs

