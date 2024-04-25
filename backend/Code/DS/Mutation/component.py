from DS.Structural.graph import Node, Edge
from DS.Structural.section import Section
from DS.Temporal.time import Time
from Interfaces.cost import Cost
from Utils.preferences import Preferences


class Component(Cost):

    """
    Analogous to the Section class unifying common properties of Edges and Nodes, this unifies properties of Segments and Intersections
    A Component is like a "personalized Section", harboring an additional incidence Time and user Preferences
    """

    def __init__(self, part:Section, prefs:Preferences, incidence:Time):
        self.part = part
        self.incidence = incidence
        self.preferences = prefs

    def cost(self):
        """
        Returns the total Cost of this Component at the given Time
        This will be a weighted sum (the Preference Cost metric) of:
        - Safety (accident) risk (for the preference tolerance of Accident)
        - Distance (total length of this Component)
        - Time taken for the given Preferences' Vehicle to traverse the Component (in min) at the given incidence Time
        :return: The Cost of this Component
        """
        safety, distance, time = self.preferences.metric
        return self.risk()*safety + self.part.length*distance + self.elapsed()*time

    def elapsed(self):
        """
        Returns the time taken by the given Preferences to cover the Component
        :return: The time (in minutes) taken by
        """
        veh = self.preferences.vehicle
        inc = self.incidence
        temporal = self.part.stats.flows[veh].value(inc)
        return temporal # Time taken for this vehicle to cover the Component

    def completion(self):
        """
        Returns the Time upon completing the Component
        :return: The time upon completing the Component
        """
        t = Time()
        t.set(self.elapsed())
        result = t + self.incidence
        return result # Of type Time

    def risk(self):
        """
        Return the chance of an accident based on the current Component, including user Preferences.
        We assume accidents are independent of distance length, thus this placement.
        :return:
        """
        return 0 # TODO METHOD STUB


class Intersection(Component):

    """
    Represents the Path analogue of a Node
    """

    def __init__(self, node:Node, preferences:Preferences, incidence:Time):
        self.node = node
        super().__init__(node, preferences, incidence)

    def domain(self):
        """
        Represents the set of Intersection which may be reachable from this Intersection
        :return: The set of Intersection reachable from this Intersection
        """
        potential = []
        for edge, node in self.node.domain():
            seg = Segment(edge, self.preferences, self.completion())
            ins = Intersection(node, self.preferences, seg.completion())
            potential.append((seg, ins, seg.cost() + ins.cost()))
        return potential


class Segment(Component):

    """
    A Segment represents the Path analogue of an Edge
    A Segment is associated with an Edge in a Graph but possesses qualities similar to a Component
    """

    def __init__(self, edge:Edge, preferences:Preferences, incidence:Time):
        super().__init__(edge, preferences, incidence)

