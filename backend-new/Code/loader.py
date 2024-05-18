"""
Class designed to set up the base traffic network with all accidents & traffic flows, with preloaded times & distances
It is only called once to completely set up the traffic network, which is then serialized to disk for more effective access
Nonetheless, some relevant functions may be called more than once

This class consists of the following methods:
 - create(): Creates the traffic network for the chosen location
 - prepare(network): Adds the initial data template to nodes and edges
 - load_accidents(network): Loads all OpenOttawa accidents to the network
 - load_flows(network): Loads all OpenOttawa traffic flows to the network
 - extract_flows(network, filenames, assessing_segment=True): Extracts all flows from the network dependent on whether it's an edge or node
 - load_gadgets(network): Adds all gadgets from an Overpass API query and OpenOttawa data
 - compute_risks(network): Computes the risk of a chosen accident policy
 - compute_costs(network, metric=Cost.STANDARD): Assigns costs to an edge of the network
 - travel_times(network): Assigns travel times to each edge
 - setup(): Sets up the network through calling all of the above
 - load(): Loads the network but serializes data such that its params are converted to their true type
 - LOADED_TRAFFIC_NETWORK: The true base traffic network to operate on.
"""

from __future__ import annotations # To allow prior typecheck on Cost __add__ method

import collections
import copy
import csv
import datetime
import math

import networkx
import overpy
import osmnx

import constants
from Code.Accident.accident import Accident
from Code.Atomic.gadget import Gadget
from Code.Atomic.vehicle import Vehicle
from Code.Interfaces.cost import Cost
from Code.filenames import Filenames

# The traffic network consists of four major parameters
# distance: float
# time: float
# accidents: [Accident]
# flows: int

def create():
    """
    :return: The base network, in this case, the standard traffic network for the National Capital Region (NCR)
    """
    return osmnx.graph_from_place(constants.LOCATIONS, network_type=constants.FEATURES[0])
def prepare(network:networkx.MultiDiGraph):
    """
    :param network: The base network to operate on
    :return: Prepares the network by adding placeholder information of the initial template, to the network's nodes and edges
    """
    # We can also set each node to have standard expected intersection length for more accurate answers
    networkx.set_node_attributes(network, {node:constants.INTERSECTION_LENGTH for node in network}, 'length')
    networkx.set_node_attributes(network, {node: copy.deepcopy(constants.INIT_TEMPLATE) for node in network.nodes})
    networkx.set_edge_attributes(network, {edge: copy.deepcopy(constants.INIT_TEMPLATE) for edge in network.edges})
def load_accidents(network):
    """
    Load all accident from OpenOttawa traffic collision csv dataset to edges along traffic network, and only edges.
    This is done so to improve computation speed and factor them into OSMnx sole edge incorporation algorithms.
    :param network: The network to add accidents to
    :return: Adds the accidents to the network and returns nothing
    """

    afn = Filenames.collisiondata()
    lat_s, long_s, acc_list = [], [], [] # (lat, long) pairs with corresponding accidents

    accidents_parser = csv.reader(open(afn))
    next(accidents_parser) # Skip useless header
    for line in accidents_parser: # Parse lat, long, acc from line
        lat_s += [float(line[0])]
        long_s += [float(line[1])]
        acc = Accident()
        acc.parse(afn, line)
        acc_list += [acc]
    edge_list = osmnx.nearest_edges(network, long_s, lat_s) # The closest edge to each accident
    assert len(edge_list) == len(acc_list) # Sanity check

    # Pair each edge with list of accidents corresponding to that edge
    edge_accidents = collections.defaultdict(lambda: copy.deepcopy(constants.ACCIDENTS_DEFAULT))
    for i in range(len(edge_list)):
        edge_accidents[edge_list[i]] += [acc_list[i]]
    networkx.set_edge_attributes(network, edge_accidents, 'accidents') # Set final edge attributes
def load_flows(network):

    """
    Load measured traffic flows from the mid-block and intersection OpenOttawa datasets to the traffic network
    Assume fixed flow otherwise; it is possible for the network to be "inconsistent" if nodes are sources or sinks
    :param network: The traffic network to modify
    :return: The flows attached to this traffic network
    """

    # Load both segments and intersections
    extract_flows(network, True)
    extract_flows(network, False)
def extract_flows(network, assessing_segment:bool = True): # TODO Add consistent flow distribution process
    """
    Helper method extracting network flows from a particular fileset based on indicator of its component part (segment or intersection)
    These two methods are identical excepting osmnx.set_edge or osmnx.set_node finishing methods, respectively
    :param network: The network to place flow on
    :param assessing_segment: Whether assessing road segment or intersection
    :return: Extracts the flows from the filename and assigns them to the network
    """

    filenames = Filenames.midblockvols() if assessing_segment else Filenames.intersectvols() # List of all filenames

    pts_lat, pts_long, associated_data = [], [], [] # (lat, long) with time-independent flow breakdown

    for year in filenames:
        filename_year = filenames[year]
        if not assessing_segment and year in [2018, 2017, 2016]: # Skip years not containing all filename data
            continue
        file_yr_rdr = csv.reader(open(filename_year))
        next(file_yr_rdr) # Skip unneeded first line
        for line in file_yr_rdr: # Add coordinates and corresponding flow breakdown
            int_coord_pos = 9 if year == 2021 else 0 if year == 2015 else 8 # 2021 and 2015 have special coordinate starts
            if (assessing_segment and (line[6] == '' or line[7] == '')) or ((not assessing_segment) and (line[int_coord_pos] == '' or line[int_coord_pos + 1] == '')):
                continue  # We will avoid all pathological interpretations, this should not affect the final result
            lat, long = (float(line[6]), float(line[7])) if assessing_segment else (float(line[int_coord_pos]), float(line[int_coord_pos + 1]))
            pts_lat += [lat]
            pts_long += [long]
            associated_data += [Vehicle.OTHER.parse(filename_year, line)] # Add the vehicle breakdown

    components = osmnx.nearest_edges(network, pts_long, pts_lat) if assessing_segment else osmnx.nearest_nodes(network, pts_long, pts_lat)
    comp_avg_flows = collections.defaultdict(list) # Start with default flow set
    for i in range(len(components)):  # Ascribe each edge to a list of different traffic flows
        comp_avg_flows[components[i]] += [associated_data[i]]
    # As of now, we have a list of all components (edge or node) with different flow recordings or the default one if there is no attachment
    # The network is still consistent, as these edges or nodes can be sources or sinks (houses or buildings, for example)

    def average(flows: [{Vehicle: int}]):
        if len(flows) == 0:
            return constants.DEFAULT_VEHICLE_BREAKDOWN
        answer = {veh: 0 for veh in Vehicle.list_vehicles(0).keys()}  # Conveniently overload list vehicles method
        for instance in flows:
            answer = {veh: answer[veh] + instance[veh] for veh in answer}
        return {veh: math.ceil(answer[veh] / (len(flows)+1)) for veh in answer} # vs. len(flows) shouldn't make difference
    # Collapse list of average flows result as average of all flows along the specified edges here
    comp_avg_flows = {cmp: average(comp_avg_flows[cmp]) for cmp in comp_avg_flows}  # Can designate average flow as this result
    if assessing_segment:
        networkx.set_edge_attributes(network, comp_avg_flows, 'flows')
    else:
        networkx.set_node_attributes(network, comp_avg_flows, 'flows')

def load_gadgets(network):
    """
    Loads all Gadget from accessed Overpass API and OpenOttawa Gadget files to respective traffic network positions
    Loads Gadget on both nodes and intersections if need be
    :param network: The network to load Gadget to
    :return: Loads all Gadget to the network
    """

    # Four gadget types are added: Number Road Lanes, Speed Limit Blocks, Traffic Lights, Speed Cameras

    api = overpy.Overpass() # Use overpy mirror to OSM Overpass API for map(road) feature query data

    # Adding speed chunks as standard road-speed to nearest tenth
    osmnx.add_edge_speeds(network) # Add edge speeds to network
    speeds = networkx.get_edge_attributes(network, 'speed_kph')
    gadgets = networkx.get_edge_attributes(network, 'gadgets')
    for edge in gadgets: # Initially approximate number of gadget blocks as speed divided by frequency
        gadgets[edge][Gadget.SPEED_INCREASE] = round(speeds[edge]/Gadget.DISCRETION.value)
    networkx.set_edge_attributes(network, gadgets, 'gadgets') # The gadgets term has been modified now

    #
    # # Road lanes are already contained in network.edges(data=True)[2]['lanes']
    # # Speed limits already shown as network.edges(data=True)[2]['maxspeed']
    # # Add road lanes and speed limits as some gadgets, whenever these are modified, so are the real lanes and speed limits
    # (shown speed limit along each edge in osmnx graph, translates as gadget)

    # Get Traffic Lights via only possible Overpass API Query
    stoplight_query = """
    area[name = "Ottawa"];
    node[highway="traffic_signals"](area);
    out center;
    """ # Get coordinates of all traffic signals within geographic area
    answer = api.query(stoplight_query)
    # Functionally, traffic lights are solely at node
    nearest_nodes = osmnx.nearest_nodes(network, [float(node.lon) for node in answer.nodes], [float(node.lat) for node in answer.nodes])
    # Add number of present traffic lights to list
    amt = collections.defaultdict(lambda: copy.deepcopy(constants.DEFAULT_GADGETS_IMPLEMENTATION[Gadget.STOP_LIGHT])) # List of nodes with number of traffic lights there
    for elem in nearest_nodes:
        amt[elem] += 1

    gadgets_views = networkx.get_node_attributes(network, 'gadgets')
    for node in amt:
        gadgets_views[node][Gadget.STOP_LIGHT] += amt[node] # Add those many stoplights to gadget view
    networkx.set_node_attributes(network, gadgets_views, 'gadgets') # gadgets_views has been changed

    # Speed Enforcers
    amount = collections.defaultdict(lambda: copy.deepcopy(constants.DEFAULT_GADGETS_IMPLEMENTATION[Gadget.SPEED_ENFORCER])) # Number of speed enforcement cameras to segment
    sfn_rdr = csv.reader(open(Filenames.asecl())) # Reader of all OpenOttawa traffic locations
    next(sfn_rdr) # Skip redundant first line
    for line in sfn_rdr:
        lat, long = (float(line[3]), float(line[4]))
        road_segment = osmnx.nearest_edges(network, lat, long) # It is unreasonable and pointless to have speed cameras on intersections, so we don't include them
        amount[road_segment] = 0 if road_segment not in amount else amount[road_segment]+1
    gadget_view = networkx.get_edge_attributes(network, 'gadgets')
    for edge in amount:
        gadget_view[edge][Gadget.SPEED_ENFORCER] += amount[edge]
    networkx.set_edge_attributes(network, gadget_view, 'gadgets') # Gadget view has been updated

def deserialize(data, veh_or_gad:bool):
    """
    Deserializes the data to the respective data type, indicated by a Vehicle or Gadget. This is always trusted by the user
    Both vehicles and gadgets have the same interpretational structure
    :param data: The data to deserialize
    :param veh_or_gad: Whether a vehicle or gadget is being parsed
    :return: The respective dict of vehicles and gadgets
    """
    if not isinstance(data, str):
        return data # Probably already in desired form
    data = data[1:-1] # Remove start and end '<', '>'
    key_vals = data.split(', ')
    data = {}
    for pair in key_vals:
        itm, sep, val = pair.split(':')
        itm = itm[1:] # Remove start '<'
        form = Vehicle.for_name(itm) if veh_or_gad else Gadget.for_name(itm)
        data[form] = float(val)
    return data

def compute_risks(network):
    """
    Loads the risk of each accident occurring, or a vehicle meeting an accident, based on their traversal over that edge
    It is computed as the ratio of the number of accidents to the number of flows
    :param network: The network to compute on
    :return: The risk of accidents over the risk of flows, with a chance factor incorporated in, of being the first accident
    """
    flows = networkx.get_edge_attributes(network, 'flows')
    num_accidents = networkx.get_edge_attributes(network, 'accidents')
    # Risk is constant chance with number of previously occurred accidents
    networkx.set_edge_attributes(network, {edge:constants.CHANCE_FACTOR + len(num_accidents[edge])/sum(deserialize(flows[edge], True).values()) for edge in network.edges}, 'risk')

def compute_costs(network, metric:(float, float, float) = Cost.STANDARD):
    """
    :param network: The network to act on
    :param metric: The cost metric to optimize for
    :return: Computes the mostly-initialized network edge cost based on the cost metric and updates its edges accordingly
    """

    rc, tc, dc = metric # Get each cost
    risks_edge, time_edge, distance_edge = (networkx.get_edge_attributes(network, param) for param in ('risk', 'travel_time', 'length')) # Get each value
    networkx.set_edge_attributes(network, {seg:rc*risks_edge[seg] + tc*time_edge[seg] + dc*distance_edge[seg] for seg in network.edges}, 'cost')

    risks_node = networkx.get_node_attributes(network, 'risk')
    networkx.set_node_attributes(network, {ins:rc*risks_node[ins] + tc*constants.INTERSECTION_TRAVERSAL_TIME + dc*constants.INTERSECTION_LENGTH for ins in network.nodes}, 'cost')

def travel_times(network):
    """
    :param network: The network to act on
    :return: Adds osmnx edge travel times to the network under the key 'travel_time' for further access
    """
    networkx.set_node_attributes(network, {node:constants.INTERSECTION_TRAVERSAL_TIME for node in network.nodes}, 'travel_time')
    osmnx.add_edge_travel_times(network)

def setup():
    """
    :return: Sets up and loads the traffic network, returning individual step-completion timestamps
    """
    timestamps = {'start': datetime.datetime.now()}
    traffic_network = create()
    timestamps['create'] = datetime.datetime.now()
    prepare(traffic_network)
    timestamps['initialize'] = datetime.datetime.now()
    load_accidents(traffic_network)
    timestamps['accidents'] = datetime.datetime.now()
    load_gadgets(traffic_network)
    timestamps['gadgets'] = datetime.datetime.now()
    load_flows(traffic_network)
    timestamps['flows'] = datetime.datetime.now()
    compute_risks(traffic_network)
    timestamps['risks'] = datetime.datetime.now()
    travel_times(traffic_network)
    timestamps['times'] = datetime.datetime.now()
    compute_costs(traffic_network)
    timestamps['costs'] = datetime.datetime.now()
    osmnx.save_graphml(traffic_network, constants.TRAFFIC_NETWORK_FILEPATH)
    timestamps['save'] = datetime.datetime.now()
    return timestamps

# setup() # This is commented out to prevent loading/execution when the loaded network is cached. It should be called only upon loading for the first time.
def load():
    """
    :return: Loads the traffic network from cached graphML file and deserializes serialized string cost
    """
    network = osmnx.load_graphml(constants.TRAFFIC_NETWORK_FILEPATH)

    # Serialization causes cost params stored as str, convert all to float for graph
    # Similar prob. !w. travel_time/length due to osmnx inbuilt deserialization

    # Load all node and edge costs and deserialize them as float
    costs_edge = networkx.get_edge_attributes(network, 'cost')
    costs_node = networkx.get_edge_attributes(network, 'cost')
    networkx.set_edge_attributes(network, {edge:float(costs_edge[edge]) for edge in costs_edge}, 'cost')
    networkx.set_node_attributes(network, {node:float(costs_node[node]) for node in costs_node}, 'cost')
    return network

def interpret(graphml_network):
    """
    Accepts a loaded GraphML file of the given type, and reconstructs the network from it
    osmnx.save_graphml(network, filename) saves the graph to a GraphML file where all parameters are str.
    This method converts them back to their initial datatype.
    :param graphml_network:
    :return: Deserializes the network, converting all its data back to their original types
    """

    # Note: Gadget and Vehicle share a common deserialization method as OSMnx saves identical dict formats to GraphML in the same dict format

    cost_nodes, risk_nodes, accidents_nodes = (networkx.get_node_attributes(graphml_network, param) for param in ('cost', 'risk', 'accidents'))
    cost_edges, risk_edges, accidents_edges = (networkx.get_edge_attributes(graphml_network, param) for param in ('cost', 'risk', 'accidents'))

    flows_nodes, flows_edges = (networkx.get_node_attributes(graphml_network, 'flows'), networkx.get_edge_attributes(graphml_network, 'flows'))
    gadgets_nodes, gadgets_edges = (networkx.get_node_attributes(graphml_network, 'gadgets'), networkx.get_edge_attributes(graphml_network, 'gadgets'))

    flows_nodes, flows_edges = ({node: deserialize(flows_nodes[node], True) for node in flows_nodes}, {edge: deserialize(flows_edges[edge], True) for edge in flows_edges})
    gadgets_nodes, gadgets_edges = ({node: deserialize(gadgets_nodes[node], False) for node in gadgets_nodes}, {edge: deserialize(gadgets_edges[edge], False) for edge in gadgets_edges})

    new_node_template = {node: {'cost': float(cost_nodes[node]), 'risk': float(risk_nodes[node]), 'accidents':accidents_nodes[node], 'flows':flows_nodes[node], 'gadgets':gadgets_nodes[node]} for node in graphml_network.nodes}
    new_edge_template = {edge: {'cost': float(cost_edges[edge]), 'risk': float(risk_edges[edge]), 'accidents': accidents_edges[edge], 'flows': flows_edges[edge], 'gadgets': gadgets_edges[edge]} for edge in graphml_network.edges}

    networkx.set_node_attributes(graphml_network, new_node_template)
    networkx.set_edge_attributes(graphml_network, new_edge_template)

    return graphml_network

_TRUE_NETWORK = interpret(load()) # Private copy of true network, for reset whenever needed
LOADED_TRAFFIC_NETWORK = copy.deepcopy(_TRUE_NETWORK) # The network is now fully initialized with costs. If required, it can be edited
