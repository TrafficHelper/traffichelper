from Code.DS.Accident.accident import Accident
from Code.DS.Atomic.vehicle import Vehicle
from Code.DS.environment import Environment
from Code.DS.Mutation.component import Intersection, Segment
from Code.DS.Structural.graph import Node, Edge
from Code.DS.Temporal.time import Time
from Code.Interfaces.cost import Cost
from Code.Utils.preferences import Preferences


class Path(Cost):

    """
    A Path is a sequence of Intersection U (Edge, Intersection)n
    It represents the "personalized" version of an arbitrary Graph path
    The Path is highly modular; many of its properties depend on the constituent pairs and initial (root) Node
    """

    def __init__(self, start:Intersection, prefs:Preferences):
        self.preferences = prefs
        self.start = start.node
        self.end = start
        self.current = self.start.cost() # The current Cost of the Path at all Times
        self.steps = [] # A detailed list marking a triple of Edge, Node and cost up till then

    def cost(self):
        return self.current

    def __add__(self, following:(Edge, Node, float)) -> bool:
        e, n, c = following
        if e.outgoing != self.end.node:
            return False
        self.steps.append(following)
        self.end = n
        self.current+=c
        return True







