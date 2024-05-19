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



