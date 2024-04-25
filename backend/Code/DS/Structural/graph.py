from __future__ import annotations

import copy
import csv
from functools import cmp_to_key

from DS.Atomic.gadget import Gadget
from DS.Atomic.vehicle import Vehicle
from DS.Structural.section import Section
from DS.Structural.statistic import Statistic
from DS.Temporal.recurrence import Recurrence
from Interfaces.parser import Parser
from filenames import Filenames


class Tracker:
    """
    A Tracker consists of all data attached to a node used during the best paths Dijkstra Algorithm
    It consists of a priority queue of the user-chosen cost k, consisting of the k-best paths and the Edge, emphasis on Node pair each of them came from
    The priority queue is set to distance/cost infinity initially for all nodes
    The tracker also consists of a boolean designating when the node has been visited, as well as an option to reset it to the default tracker
    """
    INFINITY = float('inf')  # Effective Infinite cost for the purposes of this application

    def __init__(self, count:int = 0, size: int = 10):
        self.count = count
        self.size = size  # This should be Immutable
        self.optimal = self.initial()

    def update(self, new: [(float, (Node, Edge))]):
        """
        Updates the current tracker with a new set of parameters
        It accepts a new list of the best possible paths, and updates them.
        The criteria that the list be constant size is maintained
        :param new: The new list to merge
        :return: Updates the tracker to accommodate the new list
        """
        result = []
        for elem in self.optimal:
            result.append(elem)
        for elem in new:
            result.append(elem)

        def cmp(a, b):
            return 1 if a[0] > b[0] else -1 if a[0] < b[0] else 0  # Compare costs of each tuple

        result = result.sort(key=cmp_to_key(cmp))[:self.size]  # Sort with comparison to first tuple
        self.optimal = result

    def clean(self):
        self.count = 0
        self.optimal = self.initial()

    def initial(self):
        return [(Tracker.INFINITY, None)] * self.size


class Node(Section):

    """
    A Node represents an intersection in the traffic network
    A Node consists of a kernel, the Node proper, and "arms", the list of Edges incoming (having their ends) in it, and outgoing (starting in it)
    A Node is also equipped with a list of Gadget
    A Node has the same Statistics as an Edge and is also a Section like an Edge, but possesses (functionally) zero length
    Node and Node are only equal if they are identical
    """

    def __init__(self, stats: Statistic = None, gadgets: [Gadget] = None):
        # Edges going into and coming out of the node
        self.incoming = {*()}
        self.outgoing = {*()}

        self.tracker = Tracker() # Tracking the node's status, used in the application TODO Fix this
        super().__init__(stats, gadgets)

    def __hash__(self): # Hash method for O(n) set addition algorithm
        return hash(self.incoming) + hash(self.outgoing)

    def isomorphic(self, other: Node):
        """
        Return whether the two nodes are isomorphic to each other
        Two nodes are isomorphic if the set of incoming and outgoing edges are equivalent
        :param other: The other Node to compare isomorphism with
        :return: Whether the two Node are isomorphic
        """
        return self.incoming == other.incoming and self.outgoing == other.outgoing

    def track(self, tracker:Tracker) -> Tracker:
        """
        Detaches and returns the current Tracker of the Node and attaches a new Tracker to it.
        It preserves the state of the old Tracker removed from this Node
        :param tracker: The tracker to add to this Node
        :return: The old Tracker after attaching the new one
        """
        current = self.tracker
        self.tracker = tracker
        return current

    def attach(self, road: Edge, positioning: bool) -> bool:
        """
        One of a pair of methods called when edge and node are attached to each other
        This makes one end of the edge attach itself to the node depending on how it was called.
        Returns true if the operation was successfully completed, false if the requisite road is already attached
        The Node has weaker attachment power than an Edge; a Node can merely referent the edge in itself; an Edge can make the node do so
        :param road: The Edge to add
        :param positioning: Whether we want to attach the Edge as outgoing or incoming, respectively
        :return:bool, True if the road was added successfully, False if not (ex. was already added)
        """
        if positioning:  # If we want to add edge coming out of this node
            if road in self.outgoing:
                return False
            self.outgoing.add(road)
        else:
            if road in self.incoming:
                return False
            self.incoming.add(road)
        return True

    def detach(self, road: Edge) -> bool:
        """
        Analogous to the 'attach' method
        One of a pair of methods called when edge and node are detached from each other
        This detaches the road from the specified node
        Returns true if operation successfully completed, false if road is already detached
        :param road: The road to detach from the current Node
        :return: bool, True if it was successfully detached, False otherwise (ex. was not attached)
        """

        if road in self.incoming:
            self.incoming.remove(road)
            return True
        if road in self.outgoing:
            self.outgoing.remove(road)
            return True
        return False  # Found nowhere here

    def proportions(self):

        """
       Return a vector designating each edge and the time functions of the total number of vehicles in that section
       Do this in context of the percentages of each of the elements.
       :return:
       """

        inflows: {Vehicle: Recurrence} = [ink.stats.flows for ink in self.incoming]
        outflows: {Vehicle: Recurrence} = [out.stats.flows for out in self.outgoing]

        # Sum of inflow and outflow time functions

        inside = {e: Recurrence() for e in inflows}
        for elem in inflows:
            for val in inside:
                inside[val] += inflows[elem][val]
        outside = {e: Recurrence() for e in outflows}
        for elem in outflows:
            for val in outside:
                outside[val] += outflows[elem][val]

        return inside, outside

    def refactor(self, removed: Edge): # TODO FIX

        """
       Readjusts the balance of traffic flows, traffic times and expected accidents based on the addition or removal of an Edge from the Node

       :return:
        """

        isf = [ink.stats.flows for ink in self.incoming]
        osf = [out.stats.flows for out in self.incoming]
        towards = sum(isf)
        away = sum(osf)
        # assert towards == away # If Data consistency exists
        isf = [elem / towards for elem in isf]
        osf = [elem / away for elem in osf]
        return isf, osf

    def equivalent(self, other: Node):
        """
       Checks whether two Node are equivalent
       Two Node are equivalent if their Statistic are equivalent
       :param other: the other Node to compare with
       :return: Whether the two Node are equivalent
       """
        return self.stats == other.stats

    def domain(self):
        """
        Returns the Edge-Node pair which consists of all Nodes reachable from this Node via an Edge
        This will be used by the Dijkstra Algorithm implementation
        :return: The list of all Nodes reachable from this Node via an Edge
        """
        return {edge.outgoing: edge for edge in self.outgoing}


class Edge(Section, Parser):

    """
    An Edge represents a Section which is not a Node, but like a road Segment, as part of the traffic network Graph
    Edges and Nodes combined form the traffic network
    An Edge is equipped with a set of statistics, gadgets and a name, which are the parameters with which it is called with
    However, to ensure compatibility with the OpenOttawa RoadCentrelines.csv data, it maintains three variables which designate its unique identity; toID, segID, fromID
    Each Edge is linked to two nodes representing the outgoing and incoming variables respectively. Initially they are dummy nodes; changing them occurs through the anchor method
    """

    def __init__(self, stats: Statistic = None, gadgets: [Gadget] = None, length:float = 0):

        # Which is set by observing the data
        self.length = 0

        # Open Ottawa Road IDs
        self.toID = ''
        self.segID = ''
        self.fromID = ''
        self.roadID = '' # Global Road ID

        # Length of Edge
        self.length = length

        # Start with default nonsense ends
        self.outgoing = Node(None, None) # Node Edge goes out from
        self.incoming = Node(None, None) # Node Edge enters to

        super().__init__(stats, gadgets)  # Save extra work by calling superclass with this data

    def rstar(self, start: Node) -> Node:
        """
        Reset STARt Node (outgoing) to the new node
        Return the previously attached Node
        :param start: The new Node to Reset STARt
        :return: The previously attached node
        """
        if start is None:
            raise ValueError(" Cannot rebase to Null Node ")
        current = self.outgoing
        self.outgoing = start
        return current

    def rend(self, end: Node) -> Node:
        """
        Reset END Node (incoming) to the new node
        Return the previously attached Node
        :param end: The new Node to Reset END
        :return: The previously attached Node
        """
        if end is None:
            raise ValueError(" Cannot relink to Null Node ")
        current = self.incoming
        self.incoming = end
        return current

    def parse(self, filename, data):  # TODO Finish Road Parser
        """
       Parses the edge pair from the given data line in the filename, which should be RoadCentrelines.csv
       The filename is redundant; if it is an incorrect name, it is not considered
       :param filename: The file name to parse from, which must be RoadCentrelines.csv
       :param data: The line in the file to parse from
       :return: The two one-way roads, Edge, which exist in that line of data
       """

        # Both sides of road
        alpha = Edge()
        beta = Edge()

        alpha.roadID = '' if data[29] is None else data[29]
        beta.roadID = '' if data[30] is None else data[30]

        # Create segment IDs for both sides of roads; both of them should intersect at
        alpha.segID = '' if data[31] is None else data[31]  # ROAD_NAME_ID_ODD (31)
        beta.segID = '' if data[32] is None else data[32]  # ROAD_NAME_ID_EVEN (32)

        # Create incoming and outgoing IDs for both roads
        alpha.fromID, beta.fromID = ('' if data[34] is None else data[34],) * 2  # FROM_ROAD_ID (34)
        alpha.toID, beta.toID = ('' if data[35] is None else data[35],) * 2  # TO_ROAD_ID (35)

        alpha.length, beta.length = (float(data[39]),) * 2  # No null-value check as this is always filled; both sides of road have same length

        return alpha, beta


class Graph(Parser):

    """
    Fundamentally, a Graph represents a traffic network, and is the most composite DS in the application
    This implementation of a Graph consists of a series of Nodes connected with their Edges
    A Graph is weak, in the sense that it cannot detach the Edge and Node; all contained methods which do so must make a call to those respective methods
    """

    def __init__(self):
        self.nodes: [Node] = []  # List of all nodes in Graph

    def modify(self, node: Node, add: bool = True):
        """
       Modifies the Node's position in the Graph
       If add is True, it can add it to the Graph. If the Node is already part of the Graph, it returns None, otherwise the Node to signify the successful operation
       If add is False, it can remove it from the Graph. If the Node is not part of the Graph, it returns None, otherwise returns the specified Node
       The choice of returning or not is constructed such that there exists no ambiguity among the user's choice
       :param node: The Node to modify relative to the Graph
       :param add: Whether to add or remove the Node
       :return: None|Node (see aforementioned)
       """
        # print(self.nodes)
        if add:
            if node in self.nodes:
                return None
            self.nodes.append(node)
            return node
        else:
            if node not in self.nodes:
                return None
            self.nodes.remove(node)
            return node

    def spread(self) -> {Edge}:
        """
        Returns the set of all Edge which have any connection to this Graph (any Node in it)
        :return: The set of all Edge which have any link to this Graph
        """
        edges = {*()}
        for node in self.nodes:
            # Should never have a conflict as each Edge is unique
            for edge in node.outgoing:
                edges.add(edge)
            for edge in node.incoming:
                edges.add(edge)
        return edges

    def hair(self) -> {Edge}:
        """
       Returns the hair of this Graph
       The hair of the Graph is the set of all Edge which have at least one link inside the Graph and at least one link outside the Graph
       :return: The hair of this Graph
       """
        hair = {*()}
        edges = self.spread()
        for strand in [edges[e] for e in edges]:
            if strand.incoming in self.nodes and strand.outgoing not in self.nodes or strand.outgoing in self.nodes and strand.incoming not in self.nodes:
                hair.add(strand)
        return hair

    def crop(self, strands: {Edge}, preserve:bool = True):
        """
        Crops the Graph by removing all strands.
        Either it modifies the Graph in the process(by reweighting the balance of traffic owing to the loss of the Edge)
        Or it can ignore

        :param strands: The strands to remove from the Graph
        :param preserve: Whether to re-weight the Graph assuming conservation of temporal flow or not
        :return: The Graph after the modified actions
        """

        for edge in strands:
            otg = None
            inc = None
            if edge.outgoing in self.nodes:
                otg = edge.rstar(Node(None, None))
            if edge.incoming in self.nodes:
                inc = edge.rstar(Node(None, None))
            if not preserve:
                vehicles = [v for v in Vehicle]
                vehicles.remove(Vehicle.RATIOS)
                for v in vehicles: # Refactor flows
                    volumes = edge.stats.flows[v]
                    otg.stats.flows[v] = otg.stats.flows[v] + volumes.multiply(0.5)
                    inc.stats.flows[v] = inc.stats.flows[v] + volumes.multiple(0.5)
            # Both otg and inc should be in the nodes or the Graph is not closed

    def trim(self):
        """
       Trims the graph of all hair to make it self-contained, having no hair
       De-associates the nodes with edges which link to a node not in the graph
       De-associates those respective edges from the nodes as well.
       :return:
        """
        return self.crop(self.hair())

    def deepcopy(self):
        """
        Returns a deep copy of this Graph
        Essentially copies all components of this Graph, so it is functionally equivalent, but has a different identity
        :return: A deep copy of the Graph
        """
        return copy.deepcopy(self)

    @staticmethod
    def add(dictionary, key, value): # Convenience error-safe method to add key to dict with key-list params
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)

    def parse(self, filename, data):
        """
        Parses the Graph from the RoadCentrelines.csv file
        It is parsed from scratch, i.e. this is a self-contained method
        Rather than placing two separate parsing methods in the Edge and Node classes, this exploits local symmetry to improve efficiency
        :param filename: The (redundant) filename to parse, must be RoadCentrelines.csv
        :param data: The (redundant) data to parse, it is not considered
        :return: A Graph formed from the data
        """

        fn = Filenames.centrelines()

        # Dict of all roads with Edge as the value, ordered with keys as identity of road they are
        rds_outgoing: {str: [Edge]} = {}  # exiting from
        rds_incoming: {str: [Edge]} = {}  # going to
        rds_segments: {str: [Edge]} = {}  # possessing
        rds_embedded: {str: [Edge]} = {}  # embedded in

        # Step 1: Parse all Edges
        # Step 2: Form intersections between Edges

        with open(fn) as file:
            rdr = csv.reader(file)
            first = True
            ctr = 0 # We also maintain a counter and only take every tenth instance; this is to save time TODO Store Graph Configuration
            for line in rdr:
                if not first: #and ctr%10 == 1:
                    # Create two-way edges with reversed start and endpoints; they are part of the same road ID
                    left, right = Edge().parse(fn, line)
                    # print(left, right)
                    # print(str(left.fromID)+', '+str(left.toID)+', '+str(left.segID)+', '+str(left.roadID))
                    Graph.add(rds_outgoing, left.fromID, left)
                    Graph.add(rds_outgoing, right.fromID, right)

                    Graph.add(rds_incoming, left.toID, left)
                    Graph.add(rds_incoming, right.fromID, right)

                    Graph.add(rds_segments, left.segID, left)
                    Graph.add(rds_segments, right.segID, right)

                    Graph.add(rds_embedded, left.roadID, left)
                    Graph.add(rds_embedded, right.roadID, right)
                    # rds_outgoing[left.fromID]+=left; rds_outgoing[right.fromID]+=right
                    # rds_incoming[left.toID]+=left; rds_incoming[right.toID]+=right
                    # rds_segments[left.segID]+=left; rds_incoming[right.segID]+=right
                    # rds_embedded[left.roadID]+=left; rds_incoming[right.roadID]+=right
                ctr+=1
                first = False

        # Create association of Edges by constructing Node
        # There are three cases considered; the maximum permitted number of segments incident at an intersection is 4
        intersections:[Node] = [] # List of all Intersections
        # intersections:{*()} = {*()}
        # Case 1: There is only one segment ending there
        # In that case, the road segment will have either toID or fromID as NULL (empty)
        # Thus attach the Edge to the NULL-NODE at that end
        case_one:[Edge] = rds_incoming[''] # The list of roads which end at NULL
        for rd in case_one:
            ending_intersection = Node()
            ending_intersection.incoming.add(rd)
            intersections.append(ending_intersection)
            rd.rend(ending_intersection)

        # Case 2: Two ending segments are not considered, as it would not be an intersection

        # Case 3: Three segments intersect there
            # This occurs whenever:
            # A segment ends at another road
            # Along the intersected road, one road's incoming ends at the segment's identity and the other's outgoing, or vice versa
        # Case 4: Four segments intersect there
        for segID in rds_segments:
            seg_block = rds_segments[segID] # The list of all Edges which possess that segment id
            for directed_street in seg_block: # maximum of two such elements for two-way streets
                # Directed_street: Edge, where it begins and ends at
                brothers = rds_embedded[directed_street.roadID] # All roads the current street is common with
                fr = directed_street.fromID
                to = directed_street.toID

                if fr not in rds_embedded: # Probably link to nonexistent road
                    fr = ''
                if to not in rds_embedded: # Probably link to nonexistent road
                    to = ''

                dsrdID = directed_street.roadID # Road ID of the current directed street
                valid_segments_fr = rds_embedded[fr] # List of Edge which COULD have intersection there
                valid_segments_to = rds_embedded[to] # List of Edge which COULD contain the segment(s) the directed_street ends at

                for edge_seg in valid_segments_fr:
                    intersection = Node() # Intersection between leaving current Edge and others
                    intersection.outgoing.add(directed_street)
                    if edge_seg.toID == dsrdID: # Edge ends at that intersection
                        intersection.incoming.add(edge_seg)
                    if edge_seg.fromID == directed_street.roadID:
                        intersection.outgoing.add(edge_seg)

                    # Check whichever nodes in same edge have such endings to this road and add them too to intersection
                    # We can repeat this with the same nodes, as two nodes are identical (==) iff they are ACTUALLY identical
                    for commonality in brothers:
                        if commonality.toID == fr:
                            intersection.incoming.add(commonality)
                        if commonality.fromID == fr:
                            intersection.outgoing.add(commonality)
                    intersections.append(intersection)

                for edge_seg in valid_segments_to:
                    intersection = Node() # Intersection between incoming current Edge and others
                    intersection.incoming.add(directed_street)
                    if edge_seg.toID == dsrdID:
                        intersection.incoming.add(edge_seg)
                    if edge_seg.fromID == dsrdID:
                        intersection.outgoing.add(edge_seg)

                    # Check whichever nodes in same edge have such endings to this road and add them too to intersection
                    # We can repeat this with the same nodes, as two nodes are identical (==) iff they are ACTUALLY identical
                    for commonality in brothers:
                        if commonality.toID == fr:
                            intersection.incoming.add(commonality)
                        if commonality.fromID == fr:
                            intersection.outgoing.add(commonality)
                    intersections.append(intersection)

        # Last pass - to remove all common intersections
        # Some intersections may have been duplicated
        # HIGHLY INEFFICIENT O(n^2) algorithm # TODO Improve to O(n)

        # unique = {*()} # List of all unique intersections
        # print(intersections)
        # for i in intersections:
        #     unique.add(i)
        # print(str(intersections)+' INTE')
        # print('HERE')
        # print(len(intersections))

        print(len(intersections))
        k = 0
        for nd in intersections: # Modify the SELF due to structural requirements; takes a lot of time
            k+=1
            if k % 10000 == 0:
                print(k)
            self.modify(nd)
