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
        self.start = start
        self.end = start
        self.current = self.start.cost() # The current Cost of the Path at all Times
        self.steps = [] # A detailed list marking a triple of Edge, Node and cost up till then

    def cost(self):
        return self.current



    def __init__(self, start: Node, vehicle: Vehicle, environment: Environment, considered: [Accident], departure: Time = Time(), policy: (float, float, float) = Cost.DEFAULT):
        # Auxiliary data
        self.vehicle = vehicle
        self.environment = environment
        self.considered = considered
        self.metric = policy

        self.root = Intersection(start, self.vehicle, departure, self.environment, self.considered, self.metric)  # Root node which anchors the traversal, remains constant
        self.ending = self.root  # Last node(let) in the traversal
        self.time = self.root.timeCost()  # Time elapsed so far for the entire path

        self.endcost = self.root.cost()  # Final cost of the traversal uptil now
        self.costs = [self.endcost]  # List of all costs according to progression in the traversal

        self.traversals = []  # The list of (Segment, Intersection) groupings following the root node

        self.iter = -1  # Dummy variable for iterating over representation of self

    def __iter__(self):
        return self

    def __next__(self):
        self.iter += 1
        if self.iter == len(self.traversals):
            self.iter = -1
            raise StopIteration
        return self.traversals[self.iter]

    def push(self, other: (Edge, Node)) -> bool:
        """
       Update the path by adding another Edge and Node pair
       Returns True if the process was successfully completed, False if something obstructed it (ex. Incomplete smooth passageway)
       :param other:
       :return:
        """
        edge = other[0]
        node = other[1]
        burden = self.cost()
        if edge.outgoing != self.ending or node not in edge.incoming: return False  # Traversal must be smooth passageway between times
        link = Segment(edge, self.vehicle, self.time, self.environment, self.considered, self.metric)
        self.time += link.timeCost()
        point = Intersection(node, self.vehicle, self.time, self.environment, self.considered, self.metric)
        self.time += point.timeCost()
        self.ending = point
        linkcost = link.cost()
        pointcost = point.cost()
        self.traversals += [(link, linkcost), (point, pointcost)]
        self.costs += [(self.endcost + linkcost, self.endcost + linkcost + pointcost)]  # Update costs
        self.endcost += linkcost + pointcost
        return True

    def isroot(self):
        return len(self.traversals) == 0

    def pop(self) -> (Edge, Node):
        if self.isroot(): return ()  # Nothing to return
        pair = self.traversals.pop()
        self.ending = self.root if len(self.traversals) == 0 else self.traversals[-1][1][
            0]  # Last node of last segment-intersection pair
        self.time -= (pair[0][1] + pair[1][0])  # Sum of times in both pairs
        del self.costs[-1]
        self.endcost = self.costs[-1][0 if len(self.costs) == 1 else 1]  # Update end cost to be the last such cost
        return pair

    def end(self):
        return self.ending


    def cost(self):
        return self.endcost  # Sum of individual precomputed costs is final cost

    def threat(self):
        """
       Total chance of an accident of the prescribed type occurring along the path, computed from the independence of each of its sections
       :return:
        """
        chance = 1 - self.root.risk()
        for section in self:
            chance *= (1 - section[0][0].risk()) * (1 - section[1][0].risk())
        return 1 - chance
