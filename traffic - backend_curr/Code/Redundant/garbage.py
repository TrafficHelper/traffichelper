# All Garbage (code which was once needed, not anymore, but is still useful), goes here:

# def parse(self, filename, data):
#     """
#     Extracts the list
#     :param filename:
#     :param data:
#     :return:
#     """
#     """
#     Extract the list of nodes contained in the filename, which must be RoadCentrelines.csv
#     If the filename designates another file, it is a redundant parameter
#     :param filename: The redundant file name
#     :param data: Redundant data
#     :return: A list of nodes present in the file
#     """
#
#     file = Filenames.centrelines()
#     with open(file) as data:
#         extractor = csv.reader(data)
#         segmentOutgoing = {} # All edge pairs ordered by outgoing Edge (where they emerge from)
#         segmentIncoming = {} # All edge pairs ordered by incoming Edge (where they go into)
#         for line in extractor:
#             one, two = Edge().parse(file, line) # Pair of edges
#             segmentOutgoing[one.fromID] =
#
#
#     # RoadCentrelines.v
#
#     # RoadCentrelines.csv
#     cline = Filenames.centrelines()[0] # Should only be one RoadCentrelines.csv file
#     assert filename == cline
#     with open(cline) as data:
#         extractor = csv.reader(data)
#         for line in extractor:
#             edge = Edge().parse(Filenames.centrelines(), line)
#             # A node is an embedded triangle or square in the edge system
#             # Finding triangles and quadrilaterals;
#             # Check all links of A and all links to those links. If any include A, a triangle exists
#             # Do the same for links of A , links of those and those again. If they include A, a quadrilateral exists
#             # Edges should link to the next edge in that direction, but the two-way ness creates this ambiguity
#
#
#
#     data:[[]] = Filenames.centrelines()
#     node.length = int(float(data[39]))
#     node.
# @staticmethod
# def extract(data: {str: [[]]}):
#     """
#    Extracts all statistical data from the given file
#    The input consists of a list of lists of data attached to each string, which designates the filepath
#    All statistical data lines are assumed to already associate to the same Section (Edge or Node) and thus no checks are conducted
#    NOTE: For now we parse all data to linear recurrence time functions, this is for convenience and lack of other data
#    The data must contain collision data and mid-block or intersection volumes
#    :param data: The data to extract the flows from
#    :return: The value of the flows there
#    """
#     accidents = []
#     flows = {Vehicle.CAR: Recurrence(Time.RECURRENCE), Vehicle.MOTORCYCLE: Recurrence(Time.RECURRENCE),
#              Vehicle.TRUCK: Recurrence(Time.RECURRENCE), Vehicle.BICYCLE: Recurrence(Time.RECURRENCE),
#              Vehicle.PEDESTRIAN: Recurrence(Time.RECURRENCE)}
#     for filepath in data:
#         if filepath in Filenames.collisiondata():
#             for instance in data[filepath]:
#                 accidents += Accident(None, None, None, None, None).parse(filepath, instance)
#         if filepath in Filenames.midblockvols():  # Case 1 for flow of vehicles: Midblock volumes
#             # Currently assume Vehicle.RATIOS distribution of cars and pedestrians
#             for instance in data[filepath]:
#                 adder = [e * 7 for e in
#                          Vehicle.distribute(Vehicle.RATIOS, int(instance[3]))]  # x 7 to factor AADT_24hr_ to wk.
#                 flows[Vehicle.CAR].shift += adder[0];
#                 flows[Vehicle.MOTORCYCLE].shift += adder[1];
#                 flows[Vehicle.TRUCK].shift += adder[2]
#                 # Do some policy about bicycles or pedestrians or else assume they are zero
#         if filepath in Filenames.intersectvols():  # Case 2 for flow of vehicles: Intersection volumes
#             for instance in data[filepath]:
#                 motorized = int(data[1])
#                 trucks = int(float(data[2]) * motorized)
#                 cars = motorized - trucks
#                 pedestrians = int(data[3])
#                 bicycles = int(data[4])
#                 flows[Vehicle.CAR].shift += cars;
#                 flows[Vehicle.TRUCK].shift += trucks;
#                 flows[Vehicle.BICYCLE].shift += bicycles;
#                 flows[Vehicle.PEDESTRIAN].shift += pedestrians
#         # Calculate expected time of vehicle to base on
#         # We cannot do this until observing the density of vehicles & the length
#         return Statistic(accidents, flows, None)
#
# # @staticmethod
# # def tempest(length, flows: {Vehicle: (Recurrence, int)}) -> {Vehicle: Recurrence}:
# #
# #     """
# #    Returns the expected time taken for a list of vehicles based on their maximal speeds
# #    The flows are extended. Associated with each vehicle is a recurrence as well as its respective speed limit
# #    The average time taken is roughly length divided by maximal speed for each vehicle and decreases based on congestion;
# #    :param length:
# #    :param flows:
# #    :return:
# #    """
# #
# #     result = {}
# #     for vehicle in flows:
# #         time = length / flows[vehicle][1]  # use t = s/v to find normal time taken by vehicle
# #         # Time taken proportional to density so is time - flow normalize to [0, time]
# #         estimate = flows[vehicle].multiply(-1 * time / flows[vehicle].range()[1])
# #         estimate.shift += time
# #         result[Vehicle] = estimate
# #     return result
# def parse(self, filename, data):
# @staticmethod
# def temporal(line:str):
#     """
#     Converts
#     :param line:
#     :return:
#     """
#     date, time = line.split(' ')
#     yyyy, mm, dd = [int(comp) for comp in date.split('/')]
#     hh, nn = [int(part) for part in time.split(':')]
#     instant = date.datetime(yyyy, mm, dd, hh, nn, 0)
#     epoch = int(instant.timestamp())//60 # Minutes of epoch as absolute time
#     result = Time(); result.set(epoch) # Assume repetition of after a week
#     return result
# STD_PREC = 5  # standard precision of fourier series considered
#
# def __init__(self, precision: int = STD_PREC, period: int = PERIOD, shift: float = 0,
#              cos_coeffs: list[float] = [], sin_coeffs: list[float] = []):
#     self.precision = precision
#     self.period = period
#     self.shift = shift  # The 'k' term in the series
#     assert len(cos_coeffs) == len(
#         sin_coeffs)  # This ensures the series is balanced with all elements of same length
#     self.cos_coeffs = cos_coeffs  # All cos coefficients
#     self.sin_coeffs = sin_coeffs  # All sin coefficients
#
# @staticmethod
# def coeffs(length: int, tau: float, x: float) -> list[tuple]:
#     """
#     Computes and returns a list of all sin and cos coefficients WITHOUT their multiples, when computed at a particular position
#     Also has the value of 'tau' = 2π/p given as a helpful input
#     sc --> sin coefficients
#     cc --> cos coefficients
#     :return: A list of tuples corresponding to the cos and sin coefficients, respectively
#     """
#     coeffs = []
#     for i in range(length):
#         cos_val = math.cos(tau * (i + 1) * x)  # i + 1 since we start at 0, not good
#         sin_val = math.sqrt(1 - cos_val * cos_val)
#         coeffs.append((cos_val, sin_val))
#     return coeffs
#
# def evalTemp(self, x: float, integral: bool = False) -> float:
#     """
#     Evaluates the value of the time function at the given time, either the area (integral) or plain measure
#     :param x:
#     :param integral:
#     :return: The value of the time function depending on the code
#     """
#     scos = self.cos_coeffs
#     ssin = self.sin_coeffs
#     tau = 2 * math.pi / self.period
#     tau_inv = 1 / tau
#     ans = self.shift * (x if integral else 1)
#     cffs = Recurrence.coeffs(len(scos), tau, x)  # sin and cos coefficients evaluated
#     for i in range(len(cffs)):
#         cos_cf = scos[i] * cffs[i][0]
#         sin_cf = ssin[i] * cffs[i][1]
#         if integral:
#             cos_cf = tau_inv * ssin[i] / -(i + 1)
#             sin_cf = tau_inv * scos[i] / (i + 1)
#         ans += (cos_cf + sin_cf)
#     return ans
#
# def evaluate(self, time: float) -> float:
#     """
#     Simply evaluates the time function at the given position, and returns its value
#     :return: The value of the fourier series at the given value
#     """
#     return self.evalTemp(time)
#
# def area(self, left: float, right: float) -> float:
#     """
#     Returns the area between the left and right intervals and under the complete grouping of the fourier series
#     :param left: Left index
#     :param right: Right index
#     :return: Area between left and right intervals and under fourier series. Negative area is assumed to be discarded
#     """
#     return self.evalTemp(right, True) - self.evalTemp(left, True)
#
# def truncate(self, newPrecision: int = STD_PREC):
#     """
#     Creates a new series with identical properties as the first one, but with a new precision.
#     By default, it truncates to the standard precision.
#     :param newPrecision: The new precision to truncate to
#     :return: The series truncated to the new precision
#     """
#     if not (0 < newPrecision <= self.precision): raise ValueError(
#         "New precision must be positive, not more than current precision")
#     return Recurrence(newPrecision, self.period, self.shift, self.cos_coeffs[:newPrecision],
#                         self.sin_coeffs[:newPrecision])
#
# @staticmethod
# def interpolate(datapoints: list[tuple], period: int = PERIOD):
#     """
#     Creates and returns a fourier series proportional to the given number of datapoints
#     For a given datapoint, there must be at least 2*precision such points
#     Raises an error if not possible to interpolate
#     :param datapoints: The list of all datapoints
#     :return: A fourier series approximating to the requisite accuracy
#     """
#
#     n = len(datapoints)  # The number of datapoints that we want. We want it to be odd
#     if n == 0: raise ValueError(' No data to interpolate !')
#     if n == 1: return Recurrence(0, period, datapoints[0][1], [], [])  # Single element is linear function
#     if n % 2 == 0: datapoints = datapoints[:-1]  # Everything except last element
#     matrix = []  # Square matrix containing computed values
#     tau = 2 * math.pi / period
#     Y = [elem[1] for elem in datapoints]  # The vertical y vector
#     for elem in datapoints:
#         cffs = Recurrence.coeffs((len(datapoints) - 1) // 2, tau, elem[0])  # -1 for extra k value
#         cvect = [1]
#         for elem in cffs:  # Add alternating values of sin and cos coefficients to initial value of k
#             cvect.append(elem[0])
#             cvect.append(elem[1])
#         matrix.append(cvect)  # Create another element in the matrix
#     unknown = numpy.linalg.solve(matrix, Y)  # Should return k, a1, b1, ..., an, bn, of odd length
#     nuk = len(unknown)
#     precision = (nuk - 1) // 2
#     # Sin and cos coefficients
#     scffs = []
#     ccffs = []
#     for i in range(1, nuk, 2):
#         ccffs.append(unknown[i])
#         scffs.append(unknown[i + 2])
#     return Recurrence(precision, period, unknown[0], ccffs, scffs)
# @staticmethod
# def interpolate(datapoints: [(float, float)], period: float = Time.RECURRENCE, truncation: int = -1):
#     """
#      The series should be entirely in the upper-half plane and approximate the points to elegance (not technically interpolate them)
#      :param period:
#      :param truncation:
#      :param datapoints:
#      :return:
#     """
#
#     m = len(datapoints)
#     if m < 2 * truncation + 1:
#         raise ValueError("Not enough terms to interpolate to desired precision")
#     if truncation != -1:
#         truncation = (m - 1) / 2  # select number of truncated datapoints
#     datapoints = datapoints[:2 * truncation]  # Take only required datapoints
#     matrix = []
#     results = []
#     for point in datapoints:
#         fnt = point[1]
#         results += fnt
#         values = Recurrence.coefficients(point[0], period, truncation)
#         sina = [pair[0] for pair in values]
#         cosa = [pair[1] for pair in values]
#         row = [1]  # Zeroth term denotes k
#         row += sina
#         row += cosa
#         matrix += row
#     terms = numpy.linalg.solve(matrix, results)
#     k = terms[0]
#     terms = terms[1:]
#     sins = terms[:len(terms) / 2]
#     coss = terms[len(terms) / 2:]
#     assert len(sins) == len(coss)
#     series = Recurrence(period, float(k), [(float(sins[i]), float(coss[i])) for i in range(len(sins))])
#     return series
# def set(self, location: Section):
#     self.location = location
# # For each vehicle in outcomes, progressively iterate along numbers, if there is
# for vehicle in outcomes:
#     for number in range(len(outcomes[vehicle])):
#         current = iky[inji] # Get the current injury
#         # if len(outcomes[inji]) == 0:
#         #     inji += 1
#         #     if inji == len(injuries.keys()):
#         #         break
#
#         sub+=1
#         if sub == injuries[current]:
#             sub = 0
#         outcomes[vehicle][number] = current
#     inji+=1
# STOPLIGHT = 1
# STOPSIGN = 2
# SPEEDLIMIT(function)
# STOPLIGHT = 1
# SPEEDLIMIT = 2
# LANEDIVIDER = 3
# SPEEDBUMP = 4


# TESTING PERSISTENCE GARBAGE:

# import csv
#
# from DS.Accident.accident import Accident
# # from DS.Accident.accident import Accident
# from DS.Atomic.gadget import Gadget
# from DS.Structural.statistic import Statistic
# from DS.Temporal.recurrence import Recurrence
# # from DS.Temporal.recurrence import Recurrence
# # from DS.Accident.injury import Injury
# # from DS.Accident.outcome import Outcome
# # from DS.Atomic.vehicle import Vehicle
# # from DS.Environment.environment import Environment
# # from DS.Environment.surface import Surface
# from DS.Temporal.time import Time
# from DS.environment import Weather, Surface, Visibility, Environment
# from filenames import Filenames
# from filenames import Filenames
# def test():
#     for fn in [Filenames.collisiondata()]:
#         with open(fn) as file:
#             rdr = csv.reader(file)
#             first = True
#             for line in rdr:
#                 if not first:
#                     print(line)
#                     veh = Outcome()
#                     veh.parse(fn, line)
#                     print(veh.grading(Injury.MINOR))
#                     print(str(veh))
#                     # for elem in veh:
#                     #     if veh[elem] == 25:
#                     #         print('A')
#                     #         return 'A'
#                     print('HELLO')
#                     break
#                 first = False
#             print('DONE')

# def test():
#     for fn in [Filenames.collisiondata()]:
#         with open(fn) as file:
#             rdr = csv.reader(file)
#             first = True
#             for line in rdr:
#                 if not first:
#                     print(line)
#                     env = Environment.extract(Surface, line)
#                     print(env)
#                 first = False

# def test():
#     for fn in [Filenames.midblockvols()[2023], Filenames.intersectvols()[2023]]:
#         with open(fn) as file:
#             rdr = csv.reader(file)
#             first = True
#             for line in rdr:
#                 if not first:
#                     tm = Time().parse(fn, line)
#                     print(tm)
#                 first = False

# def test():
#     for fn in [Filenames.collisiondata()]:
#         with open(fn) as acc:
#             rdr = csv.reader(acc)
#             first = True
#             for line in rdr:
#                 if not first:
#                     acc = Accident().parse(fn, line)
#                     print(acc)
#                 first = False

# def test():
#     for fn in [Filenames.collisiondata()]:
#         lines+=
#         with (open(fn) as collisions):
#             first = True
#             rdr = csv.reader(collisions)
#             for line in rdr:
#                 if not first:
#                     s = Statistic(line)
#
#
#
#                 first = False

# def rec():
#     # r = Recurrence()
#     # r.period = 10100
#     # r.shift = 3242
#     # r.terms = [(1, 2), (9, 7), (0, 0), (0, 0), (0, 0)]
#     # r.truncate(19)
#     # print(r)
#     # s = Recurrence()
#     # s.period = 10101
#     # s.shift = 3242
#     # s.terms = [(1, 2), (9, 7)]
#     # res = (r == s)
#     # print(res)
#     r = Recurrence()
#     r.period = 10100
#     r.shift = 3242
#     r.terms = [(1, 2), (3, 4)]
#     s = Recurrence()
#     print(r.range())
#     s.period = 10100
#     s.shift = 3242
#     s.terms = r.terms
#
#     r.truncate(5)
#     print(r.value(Time(10), Time(10)))
#     print(r + s)
#     print(r - s)
#     print(r == s)
# def significance(self, gadget: Gadget):
#     """
#    Return the significance of adding or removing a gadget on this edge
#    :param gadget:
#    :return:
#    """
#
# # Convenience methods for Graph Traversal method in algorithm
# # Common to both Edges and Nodes
# def __init__(self, paths:PriorityQueue, visited:bool = False):
#     self.paths = paths
#     self.visited = visited
#
# def update(self, candidates:PriorityQueue):
#     """
#     Updates this path with the list of candidates and their data
#     Stores the k-best-paths with each other, and preserves the initial length of the priority queue
#     :param candidates:
#     :return:
#     """
#     paths = self.paths
#     candy = copy.copy(candidates)
#     self.paths = paths.meld(candy)
#
# def peek(self):
#     return self.visited
#
# def mark(self):
#     self.visited = True
#
# def unmark(self):
#     self.visited = False
# def anchor(self, start: Node, end: Node) -> (Node, Node):
#     """
#    Anchors the edge at the given outgoing and incoming nodes
#    If they're already anchored there, don't return the previous node which was anchored there.
#    :param start:
#    :param end:
#    :return:
#    """
#     entrance = None
#     escape = None
#     if start != entrance:
#         entrance = self.outgoing
#         entrance.detach(self)
#         self.outgoing = start
#     if end != escape:
#         escape = self.incoming
#         escape.detach(self)
#         self.incoming = end
#     return entrance, escape
# def __eq__(self, other:Node):
#     """
#     Return whether two nodes are identical
#     Two nodes are identical iff they are the same, i.e. represent same object (or memory location)
#     :param other: The other Node to compare with
#     :return: Whether the two Node are equal
#     """
#     return id(self) == id(other)
# def spread(self) -> set[Edge]:
#     """
#     Returns all edges which link to any node of the graph
#     :return:
#     """
#     edges = set()
#     for node in self.nodes:
#         for edge in node.outEdges:
#             edges.add(edge)
#     return edges
#
# def hair(self) -> set[Edge]:
#     """
#     Returns all edges linked to one node in the graph and another node not in the graph
#     :return:
#     """
#
#     hair = set()
#     nodes = self.nodes
#     for strand in self.spread():
#         if strand.incoming in nodes:
#             hair.add(strand)
#         if strand.outgoing in nodes:
#             hair.add(strand)
#     return hair
#
# def refactor(self, sticks: [Edge], dynamic: bool = False):
#     """
#    Functionally disassociates the selected sticks, Edges, from the Graph
#    Has the option of refactoring (predicting the newer version of) the Network to account for their removal, or doing nothing at all.
#    Due to the high cost of refactoring, it is not conducted as default.
#    :param sticks:
#    :param dynamic:
#    :return:
#    """
#     if not dynamic:
#         self.crop(sticks)
#     else:
#         for edge in sticks:
#             Node
#             innode = edge.incoming
#             proportion = innode.proportion()[edge]
#             proportion /= len(innode.proportion()) - 1
#             for elem in innode.outgoing:
#                 if elem == edge: pass
#                 elem.stats = elem.stats.replace(amount)
#             outnode = edge.outgoing
#             # Assume we distribute the p% evenly among all other edges
#
#             # Assume p% want to go somewhere
#
#         # Assume same volume, refactor vehicle flows
#         # Time taken for vehicle to cross is (functionally) proportional to number of vehicles on same road
#         # Then extrapolate accident rates involving vehicle type by old vehicle type to new vehicle type ratio

# def add(self, road:Edge, intersection:Node):
#     block = Segment(road, self.vehicle, self.time, self.environment, self.metric, self.tolerable)
#     point = Intersection(intersection, self)
#
# # def add(self, road:Edge, intersection:Node):
# #     time = self.time
# #     roadlet = Edgelet(road, self.time)
# #     intersectionelapsed = roadlet.stats.times[self.vehicle].value(self.time)
# #     intersectlet = Nodelet(intersection, intersectionelapsed)
# #     self.time+=intersectionelapsed
# #     self.time+=intersectlet.stats.times[self.vehicle].value(self.time)
# #     self.elapsed+=roadlet.cost()+intersectlet.cost()
# #     self.sequences+=(roadlet, intersectlet)
# #     return
#
# def push(self, edge: Edge, node: Node) -> bool:
#     self.sequences[]
#     current = self.
#     assert edge.incoming == node
# def expense(self):
#
#     # Adding a Node to the Graph is also permitted
#
# def expense(self):
#     """
#     Return the cost of doing the action
#     :return:
#     """
#     sec_impl_cost = 9
#     sec_rmv_cost = 4
#     gadget_impl_cost = 10
#     gadget_rmv_cost = 2
#     if self.gadget is None:
#         return self.section.cost() + (sec_impl_cost if self.directive else sec_rmv_cost)
#     return self.gadget.cost() + (gadget_impl_cost if self.directive else gadget_rmv_cost)
# def execute(self): # TODO Fix effect
#     if self.gadget is not None:
#         if self.directive:
#             self.section.gadgets.append(self.gadget)
#         else:
#             self.section.gadgets.remove(self.gadget)
#     else:
#         if not self.directive:
#             self.section.incoming = Node(None, None)
#             self.section.outgoing = Node(None, None)
# def timeCost(self):
#     return self.part.stats.times[self.conveyance].value(self.incidence)
#
# def completion(self):
#     return self.incidence + self.timeCost()
#
# def cost(self):
#     return self.metric[0]*self.risk() + self.metric[1]*self.timeCost()
# def cost(self):
#     return super().cost()
#
# def feeder(self):
#
# def reacher(self):
#     following = {}
#     reachable = self.node.reacher()
#     for path in reachable:
#
#         # path: Node:
#         following[path] =
# class Segment(Component):
#
#     def __init__(self, edge:Edge, preferences:Preferences, incidence:Time):
#         self.edge = edge
#         self.preferences = preferences
#         self.incidence = incidence
#
#     def cost(self):
#         return super().cost() + self.preferences.cost()
#
#     """
#     Represents the Segment part of a Path Component
#     """
#
#     def __init__(self, edge: Edge, conveyance: Vehicle, incidence: Time, environment: Environment, considered: [Accident] = Accident.POSSIBLE, metric: (float, float, float) = (1, 1, 1)):
#         self.length = edge.length
#         super().__init__(edge, conveyance, incidence, environment, considered, metric)
#
#     def cost(self):
#         return super().timeCost() + self.metric[2] * self.length
# def __init__(self, network:Graph):
#     """
#     Creates a utility application centered around the network
#     :param network:
#     """
#     self.network = network
#     self.updated = False # Variable for help with the bestpaths method
#
# def clear(self):
#     for node in self.network.nodes:
#         node.data.mark(False)
#         node.data.resetpq(0)
#
# def apply(self, actions:Modifications, immutable:bool = True) -> Graph|bool:
#     graph = self.network if immutable else self.network.deepcopy()
#     successful = Utils.perform(graph, actions)
#     if not successful: return False
#     if immutable: return True
#     return graph
#
# @staticmethod
# def perform(graph:Graph, actions:Modifications):
#     for action in actions.modifications:
#         trace = action.execute(graph)
#         if not trace: return False
#     return True
#
# def optimal(self, vehicle:Vehicle, env:Environment, departure:Time, start:Node, end:Node, avoid:[Edge], tolerance:[Accident] = Accident.ALL, metric:Cost, amount:int = 1) -> [Path]:
#     self.network.crop(avoid) # Functionally consider there existing no such edges in Graph without refactoring it to account for their presence
#
#
#
#     """
#     Use a variant of Djikstra's Algorithm applied to the Graph with desired Starting and Ending nodes
#     Each Edge-Node pair has an associated cost with it, make these edges of the Graph for each path.
#     Start at the center and apply BFS while maintaining a Priority Queue of the best paths found so far.
#     If any path is more expensive than the k'th best such path, avoid further exploration from it.
#     Otherwise, use the Relaxation Lemma to determine the optimal cost on each of the edges and update the PQ.
#     If the time is limited, we can DP the time too... where time is the maximum time between two points
#     For ottawa, for example, it may take, according to the measurements, 200 minutes max. Then we have a 200 x 10000 x 10000 cube
#     Above is probably infeasible, so either precompute APSP and fix cost, or use slimmed network.
#     :param vehicle:
#     :param weather:
#     :param leaveTime:
#     :param start:
#     :param end:
#     :param avoided:
#     :param metric:
#     :param numPaths:
#     :return:
#     """
#
#     self.network.refactor(avoided) # Remove unnecessary roads
#     BFS(self, start, []) # Begin BFS
#     span = max(self.network.sssp(start)) # Farthest possible time taken
#
# def BFS(self, current:Intersection, transferred:queue.PriorityQueue):
#     position = current.node
#     updated = PQ.merge(position.tracker.best, transferred, k) # Merge the best data with the current position tracker and transferred and return top k values
#     if not self.UPDATED and not updated: return
#     if updated: self.UPDATED = True # Update the Global Variable as having changed
#     position.tracker.visited = True # We have already reached this place
#     assert current in self.network.nodes
#     reachable = position.reacher() # The [Intersection:Segment] pairs which designate the next nodes reachable via the edge
#     for next in reachable:
#         cost = next.cost() + reachable[next].cost()
#         giving = position.tracker.best
#         transferred = [val + cost for val in giving] # Update all costs of the k best paths by the cost of that edge or node
#         self.UPDATED = False # Not updated anymore
#         self.BFS(next, transferred) # Move onto next node
# def __init__(self, start: Node, vehicle: Vehicle, environment: Environment, considered: [Accident], departure: Time = Time(), policy: (float, float, float) = Cost.DEFAULT):
#     # Auxiliary data
#     self.vehicle = vehicle
#     self.environment = environment
#     self.considered = considered
#     self.metric = policy
#
#     self.root = Intersection(start, self.vehicle, departure, self.environment, self.considered, self.metric)  # Root node which anchors the traversal, remains constant
#     self.ending = self.root  # Last node(let) in the traversal
#     self.time = self.root.timeCost()  # Time elapsed so far for the entire path
#
#     self.endcost = self.root.cost()  # Final cost of the traversal uptil now
#     self.costs = [self.endcost]  # List of all costs according to progression in the traversal
#
#     self.traversals = []  # The list of (Segment, Intersection) groupings following the root node
#
#     self.iter = -1  # Dummy variable for iterating over representation of self
#
# def __iter__(self):
#     return self
#
# def __next__(self):
#     self.iter += 1
#     if self.iter == len(self.traversals):
#         self.iter = -1
#         raise StopIteration
#     return self.traversals[self.iter]
#
# def push(self, other: (Edge, Node)) -> bool:
#     """
#    Update the path by adding another Edge and Node pair
#    Returns True if the process was successfully completed, False if something obstructed it (ex. Incomplete smooth passageway)
#    :param other:
#    :return:
#     """
#     edge = other[0]
#     node = other[1]
#     burden = self.cost()
#     if edge.outgoing != self.ending or node not in edge.incoming: return False  # Traversal must be smooth passageway between times
#     link = Segment(edge, self.vehicle, self.time, self.environment, self.considered, self.metric)
#     self.time += link.timeCost()
#     point = Intersection(node, self.vehicle, self.time, self.environment, self.considered, self.metric)
#     self.time += point.timeCost()
#     self.ending = point
#     linkcost = link.cost()
#     pointcost = point.cost()
#     self.traversals += [(link, linkcost), (point, pointcost)]
#     self.costs += [(self.endcost + linkcost, self.endcost + linkcost + pointcost)]  # Update costs
#     self.endcost += linkcost + pointcost
#     return True
#
# def isroot(self):
#     return len(self.traversals) == 0
#
# def pop(self) -> (Edge, Node):
#     if self.isroot(): return ()  # Nothing to return
#     pair = self.traversals.pop()
#     self.ending = self.root if len(self.traversals) == 0 else self.traversals[-1][1][
#         0]  # Last node of last segment-intersection pair
#     self.time -= (pair[0][1] + pair[1][0])  # Sum of times in both pairs
#     del self.costs[-1]
#     self.endcost = self.costs[-1][0 if len(self.costs) == 1 else 1]  # Update end cost to be the last such cost
#     return pair
#
# def end(self):
#     return self.ending
#
#
# def cost(self):
#     return self.endcost  # Sum of individual precomputed costs is final cost
#
# def threat(self):
#     """
#    Total chance of an accident of the prescribed type occurring along the path, computed from the independence of each of its sections
#    :return:
#     """
#     chance = 1 - self.root.risk()
#     for section in self:
#         chance *= (1 - section[0][0].risk()) * (1 - section[1][0].risk())
#     return 1 - chance
#
#
# @staticmethod
# def voload(network, edges, gid):
#     """
#     Acronym for VOlume LOAD, loads the volumes from both the midblock and intersectional files to the network
#
#     :param edges:
#     :param gid:
#     :return:
#     """
#
#
# @staticmethod
# def load():
#     """
#     Loads all parsed data into the Graph representing the traffic network
#     :return: Graph representing all parsed data
#     """
#
#     # Step 1: Load network structure
#     network = Graph()
#     network.parse(Filenames.centrelines(), [])
#
#     edges = network.spread()
#
#     # Step 2: Load Accident Data
#     acf = Filenames.collisiondata()
#     with open(acf) as accidents:
#         rdr = csv.reader(accidents)
#         first = True
#         for line in rdr:
#             if not first:
#                 acc = Accident()
#                 acc.parse(acf, line)
#                 geoid = line[3]  # The GEO ID (Edge) of the Accident
#                 # print(random.choice(list(edges.keys())) in edges.keys())
#                 edges[random.choice(list(edges.keys()))].stats.accidents.append(acc)  # Add all accidents to edge
#             first = False
#
#     # Step 3: Load Traffic Volumes
#     tid = Filenames.intersectvols()
#     mid = Filenames.midblockvols()
#     Loader.voload(edges, tid)
#     Loader.voload(edges, mid)
#
#     # Step 4: Load all Gadgets
#
#     # # Part 1: ENFORCERS
#     # asecl = Filenames.asecl()
#     # with open(asecl) as ase:
#     #     rdr = csv.reader(ase)
#     #     first = True
#     #     for line in rdr:
#     #         if not first:
#     #             gadg =
#     #         first = False
#
#
# @staticmethod
# def voload(edges, aid):
#     """
#     Load the volumes on random edges given the edge list and file name
#     We can only load on random Edges as there is no better information present in the files
#     :param edges:
#     :param aid:
#     :return:
#     """
#     for yr in aid:
#         tyr = aid[yr]
#         with open(tyr) as feature:
#             rdr = csv.reader(feature)
#             first = True
#             for line in rdr:
#                 if not first:  # Assign flow to random Edge of Graph as we have no better information
#                     volumes = Vehicle.RATIOS.parse(yr, line)  # Breakdown of vehicle type & quantity
#                     edg = edges[edges.keys()[random.randint(0, len(edges))]]  # Random Edge selected
#                     flw = edg.stats.flows
#                     for veh in volumes:
#                         flw[veh] = Recurrence(Time.RECURRENCE, volumes[veh])
#
#     acc = Accident()
#     acc.parse()
#
#     print('DONE')
#     # print(network.nodes)
#
#     # Create user preferences
#     # prefs = Preferences(Vehicle.CAR, Environment.NORMAL, Accident.STANDARD())
