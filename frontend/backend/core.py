from enum import Enum  # Enum for traffic types
import math  # Math file for basic operations
import numpy  # Numerical-operations file
import copy  # Currently to make deep copies of Graph components


class CLI:
    """
    Class representing the CLI for the user
    """
    def __init__(self, isAdmin):
        """
        Creates a new CLI with a new event history and whether it is a superuser or not
        """
        self.history = []
        self.status = isAdmin

    def clearHistory(self):
        """
        Clears the entire history of the CLI
        :return: The cleared history of the CLI
        """
        self.history = []

    def process(self, command:str):
        """
        Processes the given command and performs the given action
        :param command: The command sequence
        :return: The given action
        """
        if len(command) == 0: return # Do nothing for no command
        command_sections = command.split(' ')
        if command_sections[0] == 'C': createActions(command_sections[1:])


class WeatherType(Enum):
    """
    Enum representing a type of weather for an accident to happen
    """
    CLEAR = 1
    FOG = 2
    RAIN = 3
    WIND = 4
    SNOW = 5

class VehicleType(Enum):
    """
    Vehicle types considered for the traffic in the traffic network (cyclists and pedestrians are considered vehicles for the application) and possibly in an accident
    """
    CAR = 1
    TRUCK = 2
    BUS = 3
    MOTORCYCLE = 4
    CYCLIST = 5
    PEDESTRIAN = 6


class TrafficGadget(Enum):
    """
    The traffic gadget types considered in the application, when elements are added or removed
    """
    STOPLIGHT = 1
    SPEEDLIMIT = 2
    LANEDIVIDER = 3


class AccidentLevel(Enum):
    """
    Accidents considered in the types, ordered by danger, or can be assigned to
    """
    UNINVOLVED = 1
    NEGLIGIBLE = 2
    MINOR = 3
    CONSIDERABLE = 4
    SERIOUS = 5  # Dangerous accidents,
    EXTREME = 6  # The most severe type of accident


class AccidentInstance:
    """
    A class encapsulating a particular accident, including:
    - The section (Node or Edge) it happened --> WE DON'T KNOW IF THIS WILL BE INCLUDED AS INFORMATION, OR TAKEN ALONG THE EDGE
    - The weather it happened in (WeatherType)
    - The outcome of the accident (AccidentLevel)
    - The time interval of the accident (between which two times it happened)
    - A vector denoting the number of vehicles of each type involved in the accident and the outcome of each such vehicle
    """

    def __init__(self, timeInterval: tuple[float, float], weather: WeatherType,
                 summary: dict[VehicleType:list[AccidentLevel]]):
        # self.section = section
        self.timeInterval = timeInterval  # The time interval is at a particular instant, only used as an interval when calling for vehicle types. Thus by standard, the elements are the same
        self.weather = weather
        self.summary = summary  # Most detailed section
        # As far as we know, the above parameters are set only when logging an accident instance


STD_PREC = 5  # standard precision of fourier series considered


def __init__(self, precision: int = STD_PREC, period: int = PERIOD, shift: float = 0,
            cos_coeffs: list[float] = [], sin_coeffs: list[float] = []):
   self.precision = precision
   self.period = period
   self.shift = shift  # The 'k' term in the series
   assert len(cos_coeffs) == len(
       sin_coeffs)  # This ensures the series is balanced with all elements of same length
   self.cos_coeffs = cos_coeffs  # All cos coefficients
   self.sin_coeffs = sin_coeffs  # All sin coefficients


@staticmethod
def coeffs(length: int, tau: float, x: float) -> list[tuple]:
   """
   Computes and returns a list of all sin and cos coefficients WITHOUT their multiples, when computed at a particular position
   Also has the value of 'tau' = 2π/p given as a helpful input
   sc --> sin coefficients
   cc --> cos coefficients
   :return: A list of tuples corresponding to the cos and sin coefficients, respectively
   """
   coeffs = []
   for i in range(length):
       cos_val = math.cos(tau * (i + 1) * x)  # i + 1 since we start at 0, not good
       sin_val = math.sqrt(1 - cos_val * cos_val)
       coeffs.append((cos_val, sin_val))
   return coeffs


def evalTemp(self, x: float, integral: bool = False) -> float:
   """
   Evaluates the value of the time function at the given time, either the area (integral) or plain measure
   :param x:
   :param integral:
   :return: The value of the time function depending on the code
   """
   scos = self.cos_coeffs
   ssin = self.sin_coeffs
   tau = 2 * math.pi / self.period
   tau_inv = 1 / tau
   ans = self.shift * (x if integral else 1)
   cffs = TimeFunction.coeffs(len(scos), tau, x)  # sin and cos coefficients evaluated
   for i in range(len(cffs)):
       cos_cf = scos[i] * cffs[i][0]
       sin_cf = ssin[i] * cffs[i][1]
       if integral:
           cos_cf = tau_inv * ssin[i] / -(i + 1)
           sin_cf = tau_inv * scos[i] / (i + 1)
       ans += (cos_cf + sin_cf)
   return ans


def evaluate(self, time: float) -> float:
   """
   Simply evaluates the time function at the given position, and returns its value
   :return: The value of the fourier series at the given value
   """
   return self.evalTemp(time)


def area(self, left: float, right: float) -> float:
   """
   Returns the area between the left and right intervals and under the complete grouping of the fourier series
   :param left: Left index
   :param right: Right index
   :return: Area between left and right intervals and under fourier series. Negative area is assumed to be discarded
   """
   return self.evalTemp(right, True) - self.evalTemp(left, True)


def truncate(self, newPrecision: int = STD_PREC):
   """
   Creates a new series with identical properties as the first one, but with a new precision.
   By default, it truncates to the standard precision.
   :param newPrecision: The new precision to truncate to
   :return: The series truncated to the new precision
   """
   if not (0 < newPrecision <= self.precision): raise ValueError(
       "New precision must be positive, not more than current precision")
   return TimeFunction(newPrecision, self.period, self.shift, self.cos_coeffs[:newPrecision],
                       self.sin_coeffs[:newPrecision])


@staticmethod
def interpolate(datapoints: list[tuple], period: int = PERIOD):
   """
   Creates and returns a fourier series proportional to the given number of datapoints
   For a given datapoint, there must be at least 2*precision such points
   Raises an error if not possible to interpolate
   :param datapoints: The list of all datapoints
   :return: A fourier series approximating to the requisite accuracy
   """


   n = len(datapoints)  # The number of datapoints that we want. We want it to be odd
   if n == 0: raise ValueError(' No data to interpolate !')
   if n == 1: return TimeFunction(0, period, datapoints[0][1], [], [])  # Single element is linear function
   if n % 2 == 0: datapoints = datapoints[:-1]  # Everything except last element
   matrix = []  # Square matrix containing computed values
   tau = 2 * math.pi / period
   Y = [elem[1] for elem in datapoints]  # The vertical y vector
   for elem in datapoints:
       cffs = TimeFunction.coeffs((len(datapoints) - 1) // 2, tau, elem[0])  # -1 for extra k value
       cvect = [1]
       for elem in cffs:  # Add alternating values of sin and cos coefficients to initial value of k
           cvect.append(elem[0])
           cvect.append(elem[1])
       matrix.append(cvect)  # Create another element in the matrix
   unknown = numpy.linalg.solve(matrix, Y)  # Should return k, a1, b1, ..., an, bn, of odd length
   nuk = len(unknown)
   precision = (nuk - 1) // 2
   # Sin and cos coefficients
   scffs = []
   ccffs = []
   for i in range(1, nuk, 2):
       ccffs.append(unknown[i])
       scffs.append(unknown[i + 2])
   return TimeFunction(precision, period, unknown[0], ccffs, scffs)

class ComponentStatistic:
    """
    Object representing aspects of the network section, including volume which passes through it, the accident rate, times taken to cross and gadgets associated
    Each section of the network, a node or an edge, has these as their components. All unique attributes are considered in the specific section instead.
    This class was derived to encapsulate all traffic information common to a node or an edge, including traffic gadgets, volume of vehicles flowing through, times taken and accidents.
    """

    def __init__(self, gadgets: list[TrafficGadget], trafficFlows: dict[VehicleType:TimeFunction],
                 times: dict[VehicleType:TimeFunction], accidents: list[AccidentInstance]):
        """
        :param gadgets: The list of traffic gadgets associated with this object
        :param volume: The volume function of each vehicle over time for this component
        :param times: The times taken for each vehicle over time for this component
        :param accidents: The list of accidents which occured along this component
        """
        self._gadgets = gadgets  # The gadgets along each route
        self.trafficFlows = trafficFlows  # The volume along the section by vehicle, over time
        self.accidents = accidents  # The list of accidents encountered by the edge or node
        self.times = times  # The times taken for each vehicle, over time. Should be similar for most vehicles, and markedly different for pedestrians and cyclists


    @property
    def gadgets(self): return self._gadgets

    @gadgets.setter
    def gadgets(self, newGadgets: list[TrafficGadget]): self._gadgets = newGadgets

    def computeRisk(self, vehicleType: VehicleType, intensity: AccidentLevel):
        

class Edge:
    """
    Class representing an edge or road in the traffic network.
    """

    def __init__(self, length: int, trafficStatistics: ComponentStatistic = None):
        """
        Edge constructor. Each edge is composed of a length and traffic statistics associated with it, and is also connected between two nodes; a starting and an ending node
        Each edge can have at most one starting node, or at most one ending node.
        :param length: The length of this edge, an integer representing meters
        :param trafficStatistics: The traffic statistics for an edge
        """
        self.length = length  # Approximated in meters to the nearest integer
        self.trafficStatistics = trafficStatistics  # All traffic statistics associated with the edge
        self._incomingNode = None
        self._outgoingNode = None

    @property
    def incomingNode(self): return self._incomingNode  # Return the incoming node (where the edge ends at, comes in to)

    @property
    def outgoingNode(
            self): return self._outgoingNode  # Return the outgoing node (where the edge begins at, emanates out from)

    @incomingNode.setter
    def incomingNode(self, newNode):
        """
        Sets the incoming node to the new node chosen, and updates that node to also include the edge.
        :param newNode:
        :return:
        """
        newNode.addOutgoingEdge(self)
        self._incomingNode = newNode

    @outgoingNode.setter
    def outgoingNode(self, newNode):
        newNode.addIncomingEdge(self)
        self._outgoingNode = newNode


# TODO fix node
class Node:
    """
    Class representing a node or intersection in the traffic network
    Like the edge, the node has the same traffic statistics as an edge which contain (hopefully) different traffic gadgets, times, etc.
    For the purposes of the application, a node, or intersection has zero length, but vehicles may still take time to transit it (via the holdup of traffic lights, for example.)
    The node differs from an edge in that it can have multiple edges coming into and going out of it. Furthermore, it is of length 0
    """

    def __init__(self, trafStats: ComponentStatistic, inVector: dict[Edge:TimeFunction] = {},
                 outVector: dict[Edge:TimeFunction] = []):
        """
        :param trafStats: The traffic statistics associated with the node
        :param inVector: The list of ALL connections the node has with edges coming into it
        :param outVector: The list of ALL connections the node has with edges coming out of it, to some other node
        """
        self.trafStats = trafStats
        self._inVector = inVector
        self._outVector = outVector

    @property
    def inVector(self): return self._inVector  # Equivalent to getting all edges which end at the given node

    @inVector.setter
    def inVector(self, newValue: dict[Edge:TimeFunction]): self._inVector = newValue  # Setting the edges to a new value at the given node

    @property
    def outVector(self): return self._outVector  # Return all edges which begin, emanate out from the given node

    @outVector.setter
    def outVector(self,newValue: dict[Edge:TimeFunction]): self._outVector = newValue  # Set the edges to a new given value

    def allEdges(self): return self.inVector | self.outVector  # Merge the two dictionaries corresponding to each edge

    def addOutgoingEdge(self, newEdge: Edge):
        outvect = self.outVector
        outvect[newEdge] = None  # TODO fix dummy variable
        self.outVector = outvect

    def removeEdge(self, edge: Edge):

    # Convenience methods
    def connectedToEdges(self): return self

    def incomingEdges(self):
        """
        Return all incoming edges to the given node
        :return: All incoming edges to the given node
        """
        return self.inVector.keys()

    def addIncomingEdge(self, newEdge: Edge):
        """
        Adds the incoming new edge to the self, graph
        :param newEdge: The new edge to the graph
        :return: True if the new edge is successfully added, false if it is already among the edges.
        """
        invect = self.inVector
        if newEdge in invect: return False
        invect[newEdge] = None  # TODO fix dummy variable
        self.inVector = invect
        return True

    def outgoingEdges(self):
        """
        Return all outgoing edges of the given node
        :return: All outgoing edges of the given node
        """
        return self.outVector.keys()

    def computeRisk(self, vehicle:VehicleType, accident:AccidentInstance, timeStart:float, timeEnd:float, period:float = PERIOD):
        """
        Computes the risk of a particular type of accident at a given time (modulo the period) for a given vehicle on the edge

        Check all similar accidents that have ever happened, and take them as the chance of one such accident happening with probability formulas applied.

        :param vehicle:
        :param accident:
        :param time:
        :param period:
        :return:
        """

        timeStart%=PERIOD
        timeEnd%=PERIOD
        if timeEnd < timeStart: timeStart-=PERIOD

        accidents = self.trafStats.accidents
        for elem in accidents: # Return an element incorporating all accidents in common, in a particular environment, modulo the total traffic flow in that time, and return it

        # total traffic flow
        totmeasure = sum([self.trafStats.trafficFlows[elems].area(timeStart, timeEnd) for elem in self.trafStats.trafficFlows)





# TODO fix graph
class Graph:
    """
    Class representing a graph or a series of nodes with their connections to each other. It is assumed that no extension exists to a node not in graph.
    The graph is the main data structure of the application. It represents the flow of traffic in the network
    """

    def __Graph__(self, nodes: list[Node], checkSelfContained: bool):
        self.nodes = nodes
        if checkSelfContained: assert self.selfContained()

    def listNodes(self):
        """
        Return a list of all nodes contained in this graph
        :return: A list of all nodes contained in this graph
        """
        return self.nodes

    def listEdges(self):
        """
        Return a list of all unique edges contained in this graph
        :return: A list of all unique edges contained in this graph
        """
        nodes = self.listNodes()
        edges = {}
        for node in nodes:
            for edge in node.incomingEdges(): edges[edge] = True
            for edge in node.outgoingEdges(): edges[edge] = True
        return edges.keys()

    def selfContained(self):
        """
        Given a graph with a list of nodes, it checks to ensure that all such nodes are connected with some other node in the graph
        :param nodes: All nodes in the graph
        :return: Whether all such nodes are connected with some other node in the graph
        """

        nodes: list[Node] = self.nodes
        for node in nodes:
            outEdges: list[Edge] = node.outgoingEdges
            for edge in outEdges: if
            edge.outgoingNode not in nodes:
            return False
            inEdges: list[Edge] = node.incomingEdges
            for edge in inEdges: if
            edge.incomingNode not in nodes:
            return False
        return True



class GraphInstant:
    """Class representing a graph at an instant of time"""

    def __init__(self, graph: Graph, time: float):


# To determine the graph at a particular instant, we know that its structure (nodes and edges) remain constant, its length also remains constant, but the component statistics do not


class Utils:
    """
    Utility class for user
    """

    def computeRisk(self, path: Path, statistics: AccidentList, level: AccidentLevel) -> float:
        """
        Compute the chance of a particular accident instance happening, i.e. at a given time along given edge or node, ..., etc.
        The risk of such a series may be determined by a bayesian-reasoning-form action. Visualizing such actions over time provides data to work on.
        :param instance: the desired type of accident to evaluate for
        :return: The risk of a particular accident instance happening along that road
        """
        return None  # TODO Method Stub

    @staticmethod
    def shortestPath(time: float, costVector: list[int], graph: Graph):
        """
        Returns the shortest path optimized according to the costVector objective along the graph, assuming starting at a given time
        :param time: The time (modulo the traffic period)
        :param costVector: The cost vector optimized by risk, distance and elapsed travel time
        :param graph: The graph to calculate at
        :return: The shortest path optimized according to the cost vector objective along the road network
        """
        specGraph = GraphInstant(graph, time)  # Create instant graph at that time


class AdminUtils:
    """
    Adiminstrator utility class
    """

    @staticmethod
    def changeIn(graph, action):
        """
        Return the change in the graph upon making some modification to the node(s)
        Works for each aspect of it
        """

    @staticmethod
    def minChange(graph, action, restrictions):
        """
        Return the minimal change in the graph requisite for some particular action.
        """


class Path:
    """
    A path represents a valid path taken by a vehicle on the road network
    A path consists of a stack of nodes and edges where:
    - The first element is always a node which the user intended to begin from
    - An edge which emanates from a node always follows it
    - A node which accepts an ingoing edge always follows it
    - The final element is always a node which the user ends at
    """

    def __init__(self):
        self.sequence = []


class UserActions:
    """
    The class of all actions taken by the user. including
    - Return a risk of a particular path
    - Return a path which optimizes a particular action
    """


class AdminActions:
    """
    The class of all actions taken by the administrator, which include all possible such actions
    - Use AIML to predict the traffic flow when a given connector is added
        - Given an edge, the following is compared:
        - Given flow at given time, calculate other
    """


class CTMC:
    """
    Class representing a continuous-time Markov Chain (CTMC), along with associated operations
    """

    def __init__(self, network: Graph):
        """
        Infers the representative matrix from the given network satisfying the kolmogorov backward equations
        :param network:
        """


class TrafficProperties(Enum):
    """
    An enum which determines the properties associated with a given vehicle
    """
    ACCIDENT_RISK = 1  # The risk of accident by vehicle, represented as a double
    TIME_TAKEN = 2  # The time taken by vehicle to cross an edge or node (intersection)
    VEHICLE_FLOW = 3  # State transistion probabilities of vehicle flow, both as a vector for a node and a matrix for complete network


class VehicleTypeProperties:
    def __init__(self, code: TrafficProperties):
        self.marker = {tp: 0 for tp in (TrafficProperties)}
        self.code = code

    def setValue(self, vehicle: VehicleType, newValue, code):
        if not code == self.code: raise TypeError('Mistake! You added the wrong type of context')
        self.marker[vehicle] = newValue


class TimeFunction:

    def __init__(self, baseShift: double, period: double, sineCoefficients: list[double], cosineCoefficients):
        self.baseShift = baseShift
        self.period = period
        assert len(sineCoefficients) == len(cosineCoefficients)
        self.sineCoefficients = sineCoefficients
        self.cosineCoefficients = cosineCoefficients

    def compute(self, time):
        sum_val = self.baseShift
        tau_p = 2 * Math.pi / self.period
        for i in range(len(self.sineCoefficients)):
            sum_val += (self.sineCoefficients[i] * Math.sin(tau_p * time * i) + self.cosineCoefficients[i] * Math.cos(
                tau_p * time * i))
        return sum_val

    def __add__(self, other: TimeFunction):
        nBaseShift = self.baseShift + other.baseShift


class VehicleRisk:
    def __init__(self, vehicleTypeAspects, ):
        self.vehicleTypeAspects


class Edge:
    def __init__(self, trafficFlow, risk, times={}, gadgets=[], length=0, incoming_edges=[], outgoing_edges=[]):
        self.incoming_node = None
        self.outgoing_node = None

        self.risk_vehicle =
        self.risk = risk
        self.times = times

        self.gadgets = gadgets
        self.length = 0

    def resetAnchor(self, incoming_or_outgoing, new_node):
        if incoming_or_outgoing:
            curr_incoming_node = self.incoming_node
            self.incoming_node = new_node
            curr_incoming_node.incoming_edges.remove(self)

        if not incoming_or_outgoing:
            curr_outgoing_node = self.outgoing_node
            self.outgoing_node = new_node
            curr_outgoing_node.outgoing_edges.remove(self)
        return True


class Node:
    def __init__(self, out_probs=[], risk=None, gadgets=None, incoming_edges=[], outgoing_edges=[]):
        self.transistion_probabilities = transistion_probabilities
        self.risk = risk
        self.gadgets = None

    def set_out_probs(self, new_probs):
        self.new_probs = new_probs


class CTMC:
    """
    A class representing a continuous-time-markov-chain (CTMC).
    See https://en.wikipedia.org/wiki/Continuous-time_Markov_chain
    Used to simulate different traffic flows
    """

    def __init__(self, matrix):

    def compute(self, time):
        return compute(self, int(time))

    def mult(self, time):
        self = identity if time % 2 == 0 else self
        time //= 2
        result = mult(self, time)
        return self * result


class Graph:
    CTMC = [[]]

    def __init__(self, ctmc=[[]], nodes=None):
        self.nodes = nodes
        self.ctmc = ctmc

    def discover(self, node, cloud):
        if node in cloud: return
        cloud[node] = True
        for elem in node.outgoing_edges: discover(self, elem.incoming_node, cloud)

    def simulate(self, time):
        CTMC_matrix = self.transistionProbabilityTotal
        time //= P
        base_matrix = CTMC_matrix
        for time_double = double_base

    def selection(self, path, vehicle):
        return 1 - mult([1 - edge.risk(vehicle) for edge in path])

    def expectedValue(self, path, vehicle):
        return 1 - mult([(1 - edge.risk(vehicle)) * expected_value(vehicle) for edge in path])

    def recompute(self, ):


class AccidentList:
    """
    A class to represent the possible risks associated with some combination of vehicles
    It consists of a series of rows in a boolean matrix, wherein each row consists of 1 or 0 depending on the vehicle involved, and the difficulty
    There is an unsupervised AI which determines the accident time, vehicles involved and edge, along with the intensity corresponding to it.
    """

    def __init__(self):
        self.table = []  # Basic table to store result

    def addInstance(self, inst: AccidentInstance):
        """
        Add a new row to the table consisting of a new row, a boolean vector involving which vehicles?, a position in the network (edge or intersection) and the result
        :param inst: the accident instance to add
        :return: None
        """
        self.table += inst

        result = self.shift * (time if toMeasure else 1)
        tau = 2 * math.pi / self.period
        trig_sum = 0
        sin_cos_vals = self.coeffs(time)
        for elem in sin_cos_vals:
            term_coeffs = [self.sin_coeffs[i], self.cos_coeffs[i]]
            if toMeasure: term_coeffs = [self.cos_coeffs[i] / (i + 1), -self.sin_coeffs[i] / (i + 1)]
            trig_sum += term_coeffs[0] * elem[0] + term_coeffs[1] * elem[1]
        trig_sum *= mul

        result += (self.sin_coeffs[i] * math.sin(multiplier * i * time) + self.cos_coeffs[i] * math.cos(
            multiplier * time))

    return result

import rough

class Path:

    def assertAlternate(self):
        """

        :return:
        """
        elems = [False if typeOf(elem) is Node for elem in self.elements]
        alternate = [elems[i] != elems[i+1] for i in range(len(elems)-1)].count(False) == 0
        return alternate # Make sure all elements alternate in the list

    def __init__(self):
        self._elements = []

    def set(self, value:Node): # Add a node
        self.elements.append(value)

    def set(self, value:Edge):
        self.elements.append(value)

    @property
    def elements(self): return self._elements
    @elements.setter
    def elements(self, other:list): self.elements = other


    def __add__(self, other:path): # Merges this path element with the other element
        base = self.elements
        for elem in other.elements: base.append(elem)
        self.elements = base

    def __sub__(self, other): # Removes the given number of elements from the path

class Utils:

    @staticmethod
    def computeRisk(car: VehicleType, path:Path, graph:Graph, time:float, period:float = PERIOD):
        return 1 - mul(graph.computeRisk(elem, car, time, period) for elem in path)

    @staticmethod
    def minPath(path:Path, graph:Graph, start:Node, end:Node, car:VehicleType, time:float, period:float = PERIOD, costVector:tuple[float] = (1, 0, 1), currCost:float = 0):
        edgeCost = {}
        for edge in start.connectedEdges and not VISITED[edge]:
            edgeCost = edge.cost(vehicle, time%period).dot(costVector)
            edgesCosts[edge] = edgeCost

        mEdge = [elem for elem in sorted(edgeCosts)[:WINDOWSIZE = 1]]
        return minPath

class ChangeSequence:

    class Change:
        """Represents a single change to the graph network"""
        def __init__(self, addRem:int = ):
    def __init__(self):
        self.actions = []


class Model:

    def bestCost(self, budget):
        # Use subset-sum algorithm
        minCost = 0
        bestAction = []
        budget = 0
        for gadget in TrafficGadget:
            for edge, node in Graph:
                if edge is Edge:
                    network.add(gadget, edge)
                    action = ['add', network, edgeIdentity]
                elif edge is Node:
                    network.add(gadget, node)
                    action = ['add', network, nodeIdentity]
                currCost = minCost - cost(network)
                if currCost > 0: # cost is lower than expected
                    budget-=currCost[budget]
                    bestAction = action
        return action