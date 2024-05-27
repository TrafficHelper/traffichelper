"""
File containing extra code snippets throughout the development process
Are not needed in the application but possibly in beta and future versions, if any
DO NOT DELETE THIS FILE!!!
"""

# # import networkx
# # import osmnx
# # import copy
# # g = osmnx.graph_from_place('Kanata North, Ottawa')
# # osmnx.plot_graph(g)
# # if __name__ == '__main__':
# # class Foo:
# #     class Bar:
# #         class Hah:
# #             def __init__(self, val):
# #                 self.val = val
# #
# #         def __init__(self, val:Hah):
# #             self.val = val
# #
# #     def __init__(self, val:Bar):
# #         self.val = val
# # obj = Foo(Foo.Bar(Foo.Bar.Hah(1)))
# # # r = copy.deepcopy(obj)
# # # obj.val.val.val = 2
# # # print(r.val.val.val)
# # # result = persistence.TRAFFIC_NETWORK
# # # print(datetime.datetime.now())
# # # st_lat, st_long = osmnx.geocode('1 Pebble Creek Crescent, Ottawa')
# # # ed_lat, ed_long = osmnx.geocode('5357 Fernbank Drive Kanata, Ottawa')
# # # print(datetime.datetime.now())
# # #
# # # a = osmnx.nearest_nodes(result, st_lat, st_long)
# # # b = osmnx.nearest_nodes(result, ed_lat, ed_long)
# # #
# # # shortest = [*osmnx.k_shortest_paths(result, a, b, 1)]
# # # osmnx.plot_graph_routes(result, shortest)
# # # def load_accidents():
# # #     """
# # #     Load all accidents to the current traffic network
# # #     :return:
# # #     """
# # #     for line in csv.reader(open(Filenames.collisiondata()))[1:]:
# # #         lat, long = (float(line[0]), float(line[1]))
# # #         edge = osmnx.nearest_edges(NETWORK, lat, long)
# # #         acc = Accident().parse(Filenames.collisiondata(), line)
# # #
# # #
# # #     edges_accidents = {} # Use default-dict to avoid if-not-in checks
# # #     first = True
# # #     for line in csv.reader(open(persistence.ACCIDENTS_FILENAME)): # First accident line is unnecessary
# # #         if not first:
# # #             lat, long = (float(line[0]), float(line[1]))
# # #             # Functionally, we will only add node data to edges, as OSMnx doesn't support adding edge data
# # #             edge = osmnx.nearest_edges(persistence.TRAFFIC_NETWORK, lat, long)
# # #             acc = Accident().parse(persistence.ACCIDENTS_FILENAME, line) # Take the interpreted accident
# # #             if edge not in edges_accidents:
# # #                 edges_accidents[edge] = []
# # #             edges_accidents[edge].append(acc) # ... And add it to the list of accidents associated with that edge
# # #         first = False
# # #     for elem in edges_accidents:
# # #         edges_accidents[elem] = {'accidents':edges_accidents[elem]}
# # #     persistence.TRAFFIC_NETWORK.add_edge()
# # #     networkx.set_edge_attributes(persistence.TRAFFIC_NETWORK, edges_accidents, 'accidents')
# # #
# # # #def load_flows():
# # import csv
# # import datetime
# #
# # # import overpy
# #
# # from Code.Accident.accident import Accident
# # from Code.filenames import Filenames
# #
# #
# # # api = overpy.Overpass()
# # # r = api.query()
# # #
# # # crd = []
# # # crd += [(float(node.lon), float(node.lat)) for node in r.nodes]
# # # crd += [(float(way.center_lon), float(way.center_lat)) for way in r.ways]
# # # crd += [(float(rel.center_lon), float(rel.center_lat)) for rel in r.relations]
# # # print(crd)
# # # print(len(crd))
# # # def parse(self, fname, data):
# # #     """
# # #     Parses the Gadget from the data present in the filename and associates it with the
# # #     So far, the filenames are:
# # #     - AutomatedSpeedEnforcementCameraLocations.csv : ENFORCER
# # #     - PedestrianCrossoverLocations.csv : CROSSOVER
# # #     - ?: STOPLIGHT --> For now we assume that if the filename is empty, it denotes a stoplight
# # #     - RedLightCameraLocations.csv : CAMERA
# # #     :param fname: The file to parse
# # #     :param data: The line in the file being parsed
# # #     :return: The Gadget in that file
# # #     """
# # #
# # #     match fname: # Simply return filename from which Gadget was obtained; trust data is from filename
# # #         case Filenames.asecl(): return Gadget.ENFORCER
# # #         case Filenames.pcl2019(): return Gadget.CROSSOVER
# # #         case Filenames.stoplights(): return Gadget.STOPLIGHT
# # #         case Filenames.rlcl(): return Gadget.CAMERA
# # # def apply(self, actions:Modification):
# # #
# # #     """
# # for edge in all_gadget_to_edges:
# #     if edge in amt:
# #         all_gadget_to_edges[edge][Gadget.STOP_LIGHT] += amt[edge]
# # networkx.set_node_attributes(network, {node:{'gadgets':all_gadget_to_edges[node]} for node in amt})
# # import datetime
# #
# # import osmnx
# #
# # from Code import loader
# # from Code.Utils.utils import Utils
# # from Code.user import User
# import csv
# from datetime import datetime
#
# import osmnx
#
# from Code.Accident.accident import Accident
# from Code.Atomic.vehicle import Vehicle
# from Code.Utils.preferences import Preferences
# from Code.Utils.utils import Utils
# from Code.filenames import Filenames
# from Code.user import User
# from Code.wrappers import AccidentWrapper
#
# # for node in nearest: # Add each traffic light to the intersection
# #     current_data = networkx.get_node_attributes(network, node)
# #     current_data['gadgets'][Gadget.STOP_LIGHT] += 1
# #     networkx.set_node_attributes(network, current_data)
#
# # gadget_view = networkx.get_edge_attributes(network, road_segment)['gadgets']# Gadget view of network
# # gadget_view[Gadget.SPEED_ENFORCER] += 1 # Increment number of speed enforcers
# # networkx.set_edge_attributes(network, {road_segment:{'gadgets':gadget_view}}) # Replace with new amount, factored for speed enforcers
# # # FIND TRAFFIC VOLUME ON ALL SEGMENTS
# # edges = osmnx.nearest_edges(network, segment_long, segment_lat)
# # edges_avg_flows = collections.defaultdict(list)
# # for i in range(len(edges)): # Ascribe each edge to a list of different traffic flows
# #     edges_avg_flows[edges[i]].append(associated_data[i])
# #
# # def addition(flows:[{Vehicle:int}]):
# #     answer = {veh:0 for veh in Vehicle.list_vehicles(0).keys()} # Conveniently overload list vehicles method
# #     for instance in flows:
# #         answer = {veh: answer[veh] + instance[veh] for veh in answer}
# #     return {veh: math.ceil(answer[veh]/len(answer)) for veh in answer}
# #
# # edge_gadgets = networkx.get_edge_attributes(network, 'gadgets')
# # result = {edge:addition(edges_avg_flows[edge]) for edge in edges_avg_flows} # Can designate average flow as this result
# # modified = {edge:None for edge in result}
# # for edge in result: # Inject this into the greater scheme of gadgets
# #     current = edge_gadgets[edge] # List of gadgets
# #     current['flows'] = result[edge]
# #     modified[edge] = current
# # networkx.set_edge_attributes(network, modified, 'gadgets')
#
# # FIND TRAFFIC VOLUME ON ALL INTERSECTIONS
#
# # intersection_lat, intersection_long, associated_data = extract_flows(Filenames.intersectvols())
# # intersect_avg_flows = collections.defaultdict(list)
# # intersection_filenames = Filenames.intersectvols()
# # # The list of all intersection latitudes and longitudes considered
# # intersect_lat = []
# # intersect_long = []
# # associated_intersection_data = [] # The vehicle flows/breakdowns parsed, same length as above two
# # for year in intersection_filenames:
# #     filename_year = intersection_filenames[year]
#
# # import csv
# #
# # import osmnx
# #
# # from Code import loader
# # from Code.Accident.accident import Accident
# # from Code.filenames import Filenames
# #
# #
# # def domain():
# #     print('Hello')
# #     first = True
# #     afn = Filenames.collisiondata()
# #     lst = {*()}
# #     i = 0
# #     for line in csv.reader(open(afn)):
# #         print('A')
# #         if first:
# #             first = False
# #             continue
# #         r = Accident()
# #         r.parse(afn, line)
# #         print(r)
# #         i+=1
# #         print(i)
# #         lst.add(r)
# #     print(lst)
# # # domain()
# # print('start')
# # # r = loader.LOADED_TRAFFIC_NETWORK
# # print('end')
# # # osmnx.plot_graph(r)
# #     # Step 2: Recompute risks
# #     loader.compute_risks(self.curr_network)
# #
# # # Change the new implicit risk
# # current_risks = networkx.get_edge_attributes(self.curr_network, 'risk') # The risk parameters for our default assessment of accidents
# # new = {edge:current_risks[edge]*valid_accidents/len(accidents) for edge in self.curr_network.edges} # The new risk is the risk divided by the ratio of accidents eliminated to original accidents
# # networkx.set_edge_attributes(self.curr_network, new, 'risk') # Set the network's risk attributes to the newly computed ones
# #
# #
# #
# #
# # # Set user risks
# # # Step 1: Include only accidents which user can tolerate, or consider
# #
# # for u, v, key in self.curr_network.edges:
# #     # Step 1: Remove all accidents which are not of the tolerable type
# #     accidents_on_edge:[Accident] = self.curr_network[u][v][key]['accidents']
# #     for acc in accidents_on_edge:
# #         if acc.outcomes not in self.preferences.tolerance.outcomes:
# #             accidents_on_edge.remove(acc)
# #     self.curr_network[u][v][key]['accidents'] = accidents_on_edge
# #     # Step 2: Change the 'risk' parameter to be computed from these new types of accidents
# #     self.curr_network[u][v][key]['risk'] =
# #
# # # Step 3: Change the 'cost' factor to be dependent on the cost vector
# # #
# #
# # # All incoming edges which would redistribute to outgoing edges have some of their traffic implemented on this edge
# #
# # # Adding this edge is currently empty, flows from neighboring edges will be directed to this edge
# # # TODO We should fix this feature
# #
# # in_flows = networkx.get_edge_attributes(self.network, self.network.in_edges[u, v, key], 'flows')
# # out_flows = networkx.get_edge_attrubutes(self.network, self.network.out_edges[u, v, key], 'flows')
# # default_flows = Vehicle.OTHER.list_vehicles(
# #     100)  # The expected initial flow, by conservation of flow each edge should reduce its flow by a fixed amount
# #
# # networkx.set_edge_attributes(self.network, {self.target: copy.deepcopy(loader.INIT_TEMPLATE)})
# # networkx.set_edge_attributes(self.network, copy.deepcopy(loader.INIT_TEMPLATE))
# #
# # # Since our edge is oneway from u to v, the total flow is rebalanced among all entering edges to u and exiting edges from v
# # u_in_edges = networkx.get_edge_attributes(self.network, self.network.in_edges[u], 'flows')
# # v_out_edges = networkx.get_edge_attributes(self.network, self.network.out_edges[v], 'flows')
# # if add_or_remove:  # To add an edge
# #     self.network.add_edge(u, v, key)
# #     # Equally distribute from each of u_out_edges to n
# #     leaving = Mutation.addition([Mutation.division(u_out_edges[edge], len(u_out_edges)) for edge in
# #                                  u_out_edges])  # The total flow breakdown accorded to this edge as well
# #     # Now the outgoing edges of v will also be incremented by this flow divided by their number
# #
# #     incrementing = Mutation.division(leaving,
# #                                      len(v_out_edges))  # This is what will be added to v's outgoing edges for each edge
# #     leaving, incrementing = (
# #     Mutation.division(leaving, 2), Mutation.division(incrementing, 2))  # Divide both by 2 to smooth out over time
# #     networkx.set_edge_attributes(self.network, {self.target: incrementing}, 'flows')  # Fix joining edge
# #     # Increment flows of all out edges by given amount
# #
# # else:  # Remove one edge
# #     current_flow = networkx.get_edge_attributes(self.network, self.target, 'flows')
# #     # Remove edge (with all its gadgets too)
# #     self.network.remove_edge(u, v, key)
# #     # Increment all other flows by twice the average flow divided by that number
# #     individual_increment = Mutation.division(Mutation.division(current_flow, 1 / 2),
# #                                              len(u_out_edges) - 1)  # Decrement by one to account for removed edge
# #
# # networkx.set_edge_attributes(self.network, {})
# # networkx.set_edge_attributes(self.network, {
# #     oe: Mutation.addition([v_out_edges[oe], incrementing if add_or_remove else Mutation.negation(incrementing)]) for oe
# #     in v_out_edges}, 'flows')
#
# # a = osmnx.graph_from_place('Ottawa, Canada', network_type='drive')
# # address = osmnx.geocode('2 Pebble Creek Crescent, Ottawa')
# # b = osmnx.nearest_nodes(a, address[1], address[0])
# # print(b)
# # exit()
# # Remove unknown coordinates as preemptive check
# # for i in range(len(pts_long)): # same as len(pts_lat)
# #     if pts_long[i] == '' or pts_lat[i] == '':
# #         pts_long.remove(i)
# #         pts_lat.remove(i)
# # import networkx
# # from networkx import NetworkXError
# #
# #
# # class Graph:
# #
# #     """
# #     An application-specific encapsulation for an OSMnx networkx MultiDiGraph
# #     A Graph consists of the network body, along with
# #     - A list of nodes, with a list of Gadgets and Accidents along it
# #     - A list of edges, with a list of Gadgets and Accidents along it
# #     A Graph consists of a network, with associated node and edge lists, and the list of traffic gadgets for each one
# #     """
# #
# #     def __init__(self, network:networkx.MultiDiGraph):
# #         self.graph = network
# #
# #         self.nodes = {node:([], []) for node in network.nodes}
# #         self.edges = {edge:([], []) for edge in network.edges}
# #
# #     def add_edge(self, frm, to, edge):
# #         """
# #         Adds the given edge between the given start and finish nodes to the graph
# #         The edge contains no gadget or accident information
# #         :param frm: The start node identity
# #         :param to: The end node identity
# #         :param edge: The edge to add
# #         :return: Adds a directed edge between the start and finish nodes
# #         """
# #         self.graph.add_edge(frm, to, edge)
# #         self.edges[edge] = ([], [])
# #
# #     def remove_edge(self, frm, to, edge) -> bool:
# #         """
# #         Removes an edge from this graph.
# #         The from and to parameters are formalities
# #         :param frm:
# #         :param to:
# #         :param edge:
# #         :return:
# #         """
# #         if edge not in self.edges: # Conveniently check rather than search entire network
# #             return False
# #         self.graph.remove_edges_from([edge])
# #         del self.edges[edge]
# #         return True
# #
# #     def add_node(self, node):
# #         self.graph.add_node(node)
# #         self.nodes[node] = ([], [])
# #
# #     def remove_node(self, node) -> bool:
# #         if node not in self.nodes: # Conveniently check for associated node list instead
# #             return False
# #         # Remove all edges possibly linked to this node first
# #         for incoming in self.graph.in_edges(node):
# #             del self.edges[incoming]
# #         for outgoing in self.graph.out_edges(node):
# #             del self.edges[outgoing]
# #         self.graph.remove_node(node) # Graph dissociates these edges too
# #         del self.nodes[node]
# #         return True
# #
# #
#
#
# # NETWORK = loader.LOADED_TRAFFIC_NETWORK
# # USER = User()
# # UTILS = Utils(USER)
# #
# #
# # EXIT_COMMAND = 'exit'
# # SAVE_COMMAND = 'save'
# # SUDO_COMMAND = 'sudo'
# #
# #
# # def repl():
# #     command = ''
# #     while command != EXIT_COMMAND:
# #         command = enter_command()
# #         code = execute_command(command)
# #
# #
# # def enter_command():
# #     command = input()
# #
# # def parse_command(command):
# #     exit_command = 'exit'
# #     save_command = 'save'
# #     sudo_command = 'sudo'
# #     action, target = command.split('')
# #     if action == exit_command:
# #         exit() # Halt application if user exits terminal
# #     if action == save_command:
# #         try:
# #             osmnx.save_graphml(target)
# #
# #
# # def execute_command(command):
# #     action, target = command.split(' ')
# #     if action == :
# #
# #
# #     command = ''
# #     while command != EXIT_CMD:
# #         cmd = enter_command()
#
#
# # # Commands list
# # EXIT_CMD = 'exit'
# #
# # def run():
# #     command = ''
# #     while command != EXIT_CMD:
# #         cmd = enter_command()
# #         successful, result = execute(cmd)
# #         code = display(result)
# #         if not successful:
# #             print('Unable to parse command')
# #             continue
# #
# # def enter_command():
# #     cmd = input('>>: ')
# #
# #
# #
# # def run():
# #     # welcome()
# #     cli_setup()
# #     user_setup()
# #     utils_setup()
# #     command = ''
# #     while not command == 'EXIT':
# #         cmd = enter_command()
# #         result = execute(cmd)
# #         display(result)
# #     outro()
# #
# # def cli_setup():
# #     print('Loading network ... ')
# #     global NETWORK
# #     NETWORK = loader.LOADED_TRAFFIC_NETWORK
# #     print('Done')
# #
# # def user_setup():
# #     print('Creating normal user ... ')
# #     user = User(NETWORK)
# #     print('Done')
# #     return user
# #
# # def utils_setup():
# #     print('Creating utility function ... ')
# #     utils = Utils()
#
#
#
# # me = User()
# # tool = Utils(me)
# # me.preferences = Preferences(metric=(0, 1/2, 1/2))
# # best = tool.optimal_paths(datetime.now(), osmnx.geocode('2 Pebble Creek Crescent, Kanata, Ottawa'), osmnx.geocode('24 Sussex Drive, Ottawa'), 7)
# # print(best)
# # tool.print_paths(best)
# # for cmp in result:  # Inject this into the greater scheme of gadgets
# #     current = comp_gadgets[cmp]  # List of gadgets
# #     current['flows'] = result[cmp]
# #     modified[cmp] = current
# # """
# # # A unified interface for accessing all frequently-used objects
# # # """
# # import datetime
# #
# # import osmnx
# #
# # LOCATIONS = ['Ottawa, Canada', 'Gatineau, Canada'] # All regions considered for the application
# #
# # NETWORK_FILENAME = 'C:/Projects/trafficWise/Data/network.graphml'
# # osmnx.save_graphml(osmnx.graph_from_place(LOCATIONS, network_type='drive'), NETWORK_FILENAME)
# #
# # TRAFFIC_NETWORK = osmnx.load_graphml(NETWORK_FILENAME) # Main traffic network
# #
# # ACCIDENTS_FILENAME = 'C:/Projects/trafficWise/Data/TrafficCollisionData.csv'
# def path_roads(self, paths:[[int]]):
#     """
#     :param paths: The list of paths consisting of a squence of a sequence of integer nodeIDs/OSMids
#     :return: Converts each path in the list to an order-similar list of road names
#     """
#     gdf = osmnx.graph_to_gdfs(self.user.curr_network, nodes=False) # Convert graph to GeoDataFrame of only edges
#
#     edge_names = {} # Will represent each edge (OSMnx MultiDiGraph-compatible) with its road name
#     for _, edge in gdf.iterrows(): # Create the edge-name association
#         # print(edge)
#         # print(edge['osmid'])
#
#         node_pairs = edge['osmid']
#         name = edge['name']
#
#         if isinstance(node_pairs, int):
#             continue
#         if len(node_pairs) == 2:
#             edge_names[(node_pairs[0], node_pairs[1], 0)] = name
#         else:
#
#             edge_names[tuple(node_pairs)] = name
#     print(edge_names)
#
#     # For each route in paths, return the list of edge names for each zeroth edge connecting successive nodes
#     return [[edge_names[(u, v, 0)] for u, v in zip(route, route[1:])] for route in paths]
# gdf = osmnx.graph_to_gdfs(self.user.curr_network, nodes=False) # Should only return road edges in the network
# edges_names = {} # Create association of edges and road names
# # Create a list of all edges and their road names
# for _, edge in gdf.iterrows():
#     node_pairs = edge['osmid'] # The OSMid of an edge is an integer, nodeID pair or key
#     print(node_pairs)
#     edge_name = edge['name'] # Name of that edge
#     print(edge_name)
#     if isinstance(node_pairs, int):
#         continue # Cannot infer node position from integer
#     if len(node_pairs) == 2: # We have node coordinates
#         edges_names[(node_pairs[0], node_pairs[1], 0)] = edge_name
#     else: # Consists of three successive nodes
#         edges_names[(node_pairs[0], node_pairs[1], 0)] = edge_name
#         edges_names[(node_pairs[1], node_pairs[2], 0)] = edge_name
# print(edges_names)
# for u, v in zip(route, route[1:]):
#     if (u, v, 0) in edges_names:
#         print(edges_names[u, v, 0]["name"])
#
# from Constants.filenames import Filenames
# import csv
#
# first = True
# elements = frozenset()
# coll = Filenames.collisiondata()
#
# for line in csv.reader(open(coll)):
#     if first:
#         first = False
#         continue
#     acc = Accident()
#     acc.parse(coll, line)
#     elements = elements.union(frozenset([acc]))
# print(len(elements))

# jstr = json.dumps(query_tbl) # The JSON Query
# print(jstr)
#
# # jstr = """ {
# #     "routes": [
# #         $result
# #
# # """
# #
# # jstr = """ {
# #     "routes": [
# #         "sheldrake drive",
# #         "Hunt club road",
# #         "Viewmount Road"
# #     ],
# #     "risk": 0.5,
# #     "traveltime": 564434,
# #     "distance": 377
# #
# # } """
#
# sr = SafeRoutesResp.from_json(jstr)
# print(sr)
# return sr
# recognized = True
# assert len(components) == 1 # Only exit command
# exit()
# recognized = True
# # Show user
# if target == 'user':
#     print(self.user)
# Show graph
# import datetime
#
# import osmnx
# from networkx import MultiDiGraph
#
#
# # from Code.Utils.preferences import Preferences
#
# LOCATIONS = ["Ottawa, Canada", "Gatineau, Canada"]
# NETWORK_FILEPATH = '../Data/network.graphml'
# NETWORK = persistence.TRAFFIC_NETWORK # Was loaded once, now no need
#
# # def preload():
# #     """
# #     - Preloads the structural properties of the network obtained from the osmnx file
# #     - Saves it to disk to prevent re-computation
# #     called only once to instantiate the persistence object
# #     :return:
# #     """
# #     network = osmnx.graph_from_place(LOCATIONS)
# #     osmnx.save_graphml(network, NETWORK_FILEPATH)
#
# def optimal_paths(graph:MultiDiGraph, start_node, end_node, amount:int = 2):
#     # prf:Preferences, amount:int = 1):
#     """
#     Returns the list of optimal paths on the digraph
#     :param graph:
#     :param start_node:
#     :param end_node:
#     :param prf:
#     :param amount:
#     :return:
#     """
#
#     effective_speed_limit = {} # The effective maximal speed limit ascribable to each type, calculated from preferences
#     return [*osmnx.k_shortest_paths(graph, start_node, end_node, amount)]
#
# def extract_nodes(start:str, end:str):
#     """
#     Return the nodes corresponding to the start and end address
#     :param start: The start address
#     :param end: The end address
#     :return:
#     """
#     start_longitude, start_latitude = osmnx.geocode(start)
#     end_coord_longitude, end_coord_latitude = osmnx.geocode(end)
#     start_node = osmnx.nearest_nodes(NETWORK, start_latitude, start_longitude)
#     end_node = osmnx.nearest_nodes(NETWORK, end_coord_latitude, end_coord_longitude)
#     return start_node, end_node
#
# def overlay_paths(paths:[]):
#     """
#     Overlays the list of paths along the traffic network with transparent and slightly changing colors
#     :param paths: The list of paths to print
#     :return: The paths over-layered on the traffic network. They are also zoomed to scale
#     """
#
#     if len(paths) == 1: # Apparently plot_graph_routes cannot accept single-element arguments
#         osmnx.plot_graph_route(NETWORK, paths[0])
#     else:
#         osmnx.plot_graph_routes(NETWORK, paths)
#
#
# def process(start_address:str, end_address:str):
#     """
#     Simulates the address extraction and best-path obtainment, while writing them to the console.
#     :param start_address: The starting address
#     :param end_address: The ending address
#     :return: The best path overlaid
#     """
#     start_node, end_node = extract_nodes(start_address, end_address)
#     best_paths = optimal_paths(NETWORK, start_node, end_node)
#     overlay_paths(best_paths)
#
#
#
#
# if __name__ == '__main__':
#
#     a = '6 Pebble Creek Crescent, Kanata, Ottawa, Canada'
#     b = '150 Elgin Street, Ottawa, Canada'
#     #show_map()
#     process(a, b)
#
#     # preload()
#
#
#
#
#
#
# from __future__ import annotations
#
# import math
#
# from Code.DS.Accident.accident import Accident
# from Code.DS.Atomic.vehicle import Vehicle
# from Code.DS.Temporal.recurrence import Recurrence
# from Code.DS.Temporal.time import Time
# from Constants.filenames import Filenames
#
#
# class Statistic:
#
#     """
#     Represents a large majority of statistical data associated with a section
#     Currently akin to a "Data Packet" of information
#     Consists of a:
#     - list of Acctmp : Density of accidents at each given time
#     - Vehicle to Recurrence flows : The frequency (in absolute number) of the vehicles on that (segment) over the measured (cyclical) time
#     - ==> Vehicle to Recurrence times : The amount of time (in minutes) it takes for a Vehicle to cross the segment of that statistic, at a given starting time
#     The Recurrence period is intended to be the standard "Time.RECURRENCE" cyclical period
#     """
#
#     def __init__(self, accidents: [Accident] = None, flows:{Vehicle:Recurrence} = None, times:{Vehicle:Recurrence} = None):
#         self.accidents = accidents
#         self.flows = flows
#         self.times = times
#
#     def __eq__(self, other: Statistic):
#         """
#         Returns whether the two types are equal to each other
#         Two Statistic are equal if they have the same accident values, flow values and time values
#         :param other: The other Statistic to compare to
#         :return: Whether the two Statistic are equal to each other
#         """
#         return self.accidents == other.accidents and self.flows == other.flows and self.times == other.times
#
#     def extract(self, accidents:[[]], midflow:[], inflow:[], myear:int = 2023, inyear:int = 2023, length:int = 30):
#         """
#         Extracts all statistical data from the given file
#         The input will consist of a list of lists of data; each one designates the statistics ostensibly related to only one Section
#         Consequently, no verification checks are conducted (this may be subject to change)
#         :param accidents: The list of all accidents to parse
#         :param midflow: The list of all flows pertaining to that segment from mid-block volumes
#         :param inflow: The list of all flows pertaining to that segment from intersection volumes
#         :param myear: The year for which midblock data was collected
#         :param inyear: The year for which intersection data was collected
#         :param length: The length of the ostensible segment this pertains to
#         :return: The parsed data
#         """
#
#         # Step 1: Record all accidents
#         troubles = []
#         fn = Filenames.collisiondata()
#         for row in accidents:
#             acc = Accident()
#             acc.parse(fn, row)
#             troubles.append(acc)
#         self.accidents = troubles # Parse accident data
#
#         # Step 2: Record all traffic flows
#         mid = [Vehicle.OTHER.parse(Filenames.midblockvols()[myear], i) for i in midflow]  # Parse vehicle densities based on mid-block flow
#         ints = [Vehicle.OTHER.parse(Filenames.intersectvols()[inyear], i) for i in inflow] # Parse vehicle densities based on intersectional flow
#         # Take vector average of all elements in final list
#
#         final = {e:0.0 for e in Vehicle}
#         del final[Vehicle.RATIOS]
#         n = len(mid) + len(ints)
#         for elem in mid:
#             for th in final:
#                 final[th]+=elem[th]
#         for elem in ints:
#             for th in final:
#                 final[th]+=elem[th]
#
#         final = {e:Recurrence(Time.RECURRENCE, math.floor(final[e]/n)) for e in final} # Due to lack of data currently cannot create nuanced recurrence
#         self.flows = final
#
#         # Step 3: Compute expected times GIVEN KNOWLEDGE OF flows
#         self.tempest(length)
#
#     def tempest(self, length:float, limit:float = 0.833):
#
#         """
#         PRIVATE METHOD
#         Given a PREVIOUSLY ASSIGNED series of traffic flows, compute the expected times for each vehicle
#         :return: The expected times for each vehicle to traverse the length given top speed
#         """
#
#         standard = length/limit # Standard time in minutes given km/min (unconventional), assuming no impediment
#         ts = {}
#         # Compute aggregate impediment
#         aggregate = Recurrence()
#         for vehicle in self.flows:
#             aggregate+=self.flows[vehicle]
#
#         lower = aggregate.range()[0]
#         # Such that the lowest possible time is the standard time; also add epsilon to account for zero as minimal range
#         aggregate = aggregate.multiply(standard/(lower + 0.01)*0.001)
#         # TODO Fix Zero division error
#
#         for vehicle in self.flows:
#             ts[vehicle] = aggregate # So far it is assumed the same for all vehicles;
#         self.times = ts
#
#     def __str__(self):
#         return 'Statistic: '+str(self.accidents) + ', flows: ' + str(self.flows) + ', times: ' + str(self.times)
#
# from __future__ import annotations
#
# import math
#
# from backend.Code.Accident.accident import Accident
# from backend.Code.Accident.outcome import Outcome
#
#
# class AccidentWrapper:
#     def __init__(self, instance:Accident):
#         self.acc = instance
#
#     def __eq__(self, other:AccidentWrapper):
#         return self.acc.outcome == other.acc.outcome and self.acc.environment == other.acc.environment
#
#     def __hash__(self):
#         return hash(OutcomeWrapper(self.acc.outcome))*hash(self.acc.environment)
#
# class OutcomeWrapper:
#     def __init__(self, out:Outcome):
#         self.out = out
#
#     def __eq__(self, other:OutcomeWrapper):
#         return self.out == other.out
#
#     def __hash__(self):
#         return math.prod([hash(veh)*math.prod([hash(elem) for elem in self.out.outcome[veh]]) for veh in self.out.outcome])
#
# # Environment doesn't need to be wrapped, as it is subclass of hashable enum
# if __name__ == '__main__':
#     fn = csv.reader(open('../Data/Volumes/IntersectVolume2015.csv'))
#     next(fn)
#     for elem in fn:
#         print(elem)
# import itertools
#
# import frozendict
# import networkx
# import osmnx
#
# from Code import loader
# import matplotlib.pyplot as plt
# import osmnx as ox
#
# nt = loader.LOADED_TRAFFIC_NETWORK
#
# def beautify(pts: [[int]]):
#     """
#     :param pts: The list of paths represented by OSMnx Node
#     :return: Converts each path to a sequence of Addresses ~ Street names, efficiency in bulk
#     """
#     global nt
#     nt = osmnx.graph_from_address('Piedmont, CA, USA')
#     r = frozendict.frozendict
#     list_rows = osmnx.graph_to_gdfs(nt, nodes=False).fillna('') # Data for each edge
#
#     for _, edge in list_rows.iterrows():
#         r.set(edge, edge['name'])
#     print(str(r))
#     print('LR' + str(list_rows))
#
#     # list_rows = {tpl[1]:list_rows[(tpl[0], tpl[1])] for tpl in list_rows}
#     result_names = []
#     for path in pts:
#         edges = [nt[this][foll][0] for this, foll in zip(path, path[1:])]
#         print(edges)
#         list_names = []
#         for edge in edges:
#             print(edge)
#             print(list_rows[edge]['name'])
#             list_names += [list_rows[edge]['name']]
#         result_names += [list_names]
#     print(result_names)
#     return result_names
#
# # ox.config(use_cache=True, log_console=True)
# #
# # G = ox.graph_from_address('Piedmont, CA, USA', dist=200, network_type='drive')
# # G = ox.get_undirected(G)
# #
# # fig, ax = ox.plot_graph(G, bgcolor='k', edge_linewidth=3, node_size=0,
# #                         show=False, close=False)
# # for _, edge in ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
# #     print(edge)
# #     c = edge['geometry'].centroid
# #     text = edge['name']
# #     ax.annotate(text, (c.x, c.y), c='w')
# # plt.show()
# # u = list(nt.nodes)[0]
# # e = nt[u]['geometries'].centroid
# # print(nt['name'])
# st_long, st_lat = osmnx.geocode('2 Pebble Creek Crescent, Kanata, Ottawa')
# end_long, end_lat = osmnx.geocode('150 Elgin Street, Ottawa')
# paths = osmnx.k_shortest_paths(nt, osmnx.nearest_nodes(nt, st_long, st_lat), osmnx.nearest_nodes(nt, end_long, end_lat), 2)
# res = beautify(paths)
# print(res)
# import datetime
#
# import osmnx as ox
# from geopy import Nominatim
#
#
# # def find_edges_from_osmids(graph, osmids):
# #     # Create a list to store the edges
# #     edges = []
# #
# #     # Iterate over each osmid in the route
# #     for osmid in osmids:
# #         # Iterate through all edges in the graph
# #         for u, v, key, data in graph.edges(keys=True, data=True):
# #             # Check if this edge has the same osmid as the current one in the route
# #             if 'osmid' in data and data['osmid'] == osmid:
# #                 edges.append((u, v, key))
# #                 break  # Assuming there's only one edge with this osmid, we can stop searching
# #
# #     return edges
#
#
# def get_route(address_1, address_2, place='Ottawa, Ontario, Canada'):
#     # Initialize Nominatim geocoder
#     geolocator = Nominatim(user_agent="directions_example")
#
#     # Geocode the start and end addresses
#
#     # Create a graph from the OSM data
#     graph = ox.graph_from_place(place, network_type='drive')
#
#     location_1 = geolocator.geocode(f"{address_1}, {place}")
#     location_2 = geolocator.geocode(f"{address_2}, {place}")
#     print(location_1.longitude, location_1.latitude)
#
#     # Find the nearest nodes to the geocoded locations
#     orig_node = ox.nearest_nodes(graph, location_1.longitude, location_1.latitude)
#     dest_node = ox.nearest_nodes(graph, location_2.longitude, location_2.latitude)
#
#     # Calculate the shortest path between the nodes
#     route = ox.shortest_path(graph, orig_node, dest_node, weight='length')
#
#     print(route)
#
#     # Plot the route
#     fig, ax = ox.plot_graph_route(graph, route, node_size=0)
#     return fig, ax
#
#
# # Find the route and display the plot
# start = datetime.datetime.now()
# print(start)
# fig, ax = get_route(address_1, address_2)
# end = datetime.datetime.now()
# print(end)
#
# import datetime
#
# import osmnx
#
# from Code.Accident.environment import Environment
# from Code.Atomic.vehicle import Vehicle
# from Code.Utils.preferences import Preferences
# from Code.Utils.utils import Utils
# from Code.user import User
#
# me = User()
# tool = Utils(me)
# me.preferences = Preferences(Vehicle.TRUCK, Environment.DEVIANT, (1/3, 1, 1/2))
#
# start_address = '2 Sheldrake Drive, Ottawa, Canada'
# start_lat, start_long = osmnx.geocode(start_address)
#
# end_address = '1755 Merivale Road, Ottawa, Canada'
# end_lat, end_long = osmnx.geocode(end_address)
#
# number_paths = 10
#
# best_paths = tool.optimal_paths(datetime.datetime.now(), (start_lat, start_long), (end_lat, end_long), number_paths)
# for path in best_paths:
#     print(str(path) + ':' + str(best_paths[path]))
# tool.print_paths(best_paths)
# first = True
# elements = {*()}
# coll = Filenames.collisiondata()
# for line in csv.reader(open(coll)):
#     if first:
#         first = False
#         continue
#     acc = Accident()
#     acc.parse(coll, line)
#     elements.add(acc)
# return elements
# Install all dependencies from requirements.txt
#
# Running the program:
#
# Preliminary setup:
#
#
#
# 1. Running the CLI: Runs the CLI without the server
#    Run on the terminal: python ../src/backend/User/main.py
#
#
# 2. Running the Server: Runs the OpenAPI server built on FastAPI
# import Gadget
# from Code.DS.Mutation.modification import Modification
# from Code.DS.Structural.graph import Edge
# from Code.Interfaces.cost import Cost
# from Code.Utils.utils import Utils
#
#
# class AdminUtils(Utils):
#
#     """
#     A class representing all actions possible to conduct ONLY by administrators.
#     An administrator has superuser privileges, being able to do all the user method available in the Utils class too.
#
#
#
#     """
#
#     def alterations(self, budget:int, gadgets:[Gadget], cost:Cost) -> Modification:
#         """
#         Returns the series of Modifications such that:
#          - All Actions of the Modifications are in the permissible Gadget
#          - The expense of the Modifications is below the budget
#          - The Graph, after applying the Modifications, has the lowest value measured by the Cost parameter
#         \nAdditionally, if one wants to restrict the modifications to particular locations, they can re-instantiate the Graph with the requisite features trimmed, and recall the function
#         :param budget: The budget of the modifications
#         :param gadgets: The constraints on the list of Gadgets permissible in the Modifications
#         :param cost: The Cost metric to measure the total new cost of the network
#         :return:
#         """
#
#    # def bestmodify(self, budget:int, gadgets:[Gadget], locations:[Edge], cost:Cost) -> Modifications:
#    #     """
#    #     Return the best Modification Sequence to apply to the (implicitly declared) network to minimize cost while remaining in budget
#    #     This is NP-Hard; even finding a sum of budgets as close as possible to the given budget limit limits the potential benefit.
#    #     For this reason, AIML is used to provide an appproximate solution to the problem
#    #     Each addition and removal of a road provides a measured difference to the cost (AIML)
#    #     Each addition and removal of a gadget on the road also provides a measurable difference (AIML)
#    #     From the current change of zero, the maximum negative value is desired. Choosing the greatest of each of these costs determines it.
#    #     We can determine, using the Knapsack problem DP algo as a consequence as well.
#    #
#    #     :param budget:
#    #     :return:
#    #     """
#    #
#    #     self.network.refactor(locations)
# The traffic network consists of four major parameters
# distance: float
# time: float
# accidents: [Accident]
# flows: int
