import datetime

import osmnx
from networkx import MultiDiGraph

import persistence

# from Code.Utils.preferences import Preferences

LOCATIONS = ["Ottawa, Canada", "Gatineau, Canada"]
NETWORK_FILEPATH = './Data/network.graphml'
NETWORK = persistence.TRAFFIC_NETWORK # Was loaded once, now no need

# def preload():
#     """
#     - Preloads the structural properties of the network obtained from the osmnx file
#     - Saves it to disk to prevent re-computation
#     called only once to instantiate the persistence object
#     :return:
#     """
#     network = osmnx.graph_from_place(LOCATIONS)
#     osmnx.save_graphml(network, NETWORK_FILEPATH)

def optimal_paths(graph:MultiDiGraph, start_node, end_node, amount:int = 2):
    # prf:Preferences, amount:int = 1):
    """
    Returns the list of optimal paths on the digraph
    :param graph:
    :param start_node:
    :param end_node:
    :param prf:
    :param amount:
    :return:
    """

    effective_speed_limit = {} # The effective maximal speed limit ascribable to each type, calculated from preferences
    return [*osmnx.k_shortest_paths(graph, start_node, end_node, amount)]

def extract_nodes(start:str, end:str):
    """
    Return the nodes corresponding to the start and end address
    :param start: The start address
    :param end: The end address
    :return:
    """
    start_longitude, start_latitude = osmnx.geocode(start)
    end_coord_longitude, end_coord_latitude = osmnx.geocode(end)
    start_node = osmnx.nearest_nodes(NETWORK, start_latitude, start_longitude)
    end_node = osmnx.nearest_nodes(NETWORK, end_coord_latitude, end_coord_longitude)
    return start_node, end_node

def overlay_paths(paths:[]):
    """
    Overlays the list of paths along the traffic network with transparent and slightly changing colors
    :param paths: The list of paths to print
    :return: The paths over-layered on the traffic network. They are also zoomed to scale
    """

    if len(paths) == 1: # Apparently plot_graph_routes cannot accept single-element arguments
        osmnx.plot_graph_route(NETWORK, paths[0])
    else:
        osmnx.plot_graph_routes(NETWORK, paths)


def process(start_address:str, end_address:str):
    """
    Simulates the address extraction and best-path obtainment, while writing them to the console.
    :param start_address: The starting address
    :param end_address: The ending address
    :return: The best path overlaid
    """
    start_node, end_node = extract_nodes(start_address, end_address)
    best_paths = optimal_paths(NETWORK, start_node, end_node)
    overlay_paths(best_paths)




if __name__ == '__main__':

    a = '6 Pebble Creek Crescent, Kanata, Ottawa, Canada'
    b = '150 Elgin Street, Ottawa, Canada'
    #show_map()
    process(a, b)

    # preload()






