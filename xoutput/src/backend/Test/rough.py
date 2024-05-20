import datetime

import osmnx as ox
from geopy import Nominatim


# def find_edges_from_osmids(graph, osmids):
#     # Create a list to store the edges
#     edges = []
#
#     # Iterate over each osmid in the route
#     for osmid in osmids:
#         # Iterate through all edges in the graph
#         for u, v, key, data in graph.edges(keys=True, data=True):
#             # Check if this edge has the same osmid as the current one in the route
#             if 'osmid' in data and data['osmid'] == osmid:
#                 edges.append((u, v, key))
#                 break  # Assuming there's only one edge with this osmid, we can stop searching
#
#     return edges


def get_route(address_1, address_2, place='Ottawa, Ontario, Canada'):
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="directions_example")

    # Geocode the start and end addresses

    # Create a graph from the OSM data
    graph = ox.graph_from_place(place, network_type='drive')

    location_1 = geolocator.geocode(f"{address_1}, {place}")
    location_2 = geolocator.geocode(f"{address_2}, {place}")
    print(location_1.longitude, location_1.latitude)

    # Find the nearest nodes to the geocoded locations
    orig_node = ox.nearest_nodes(graph, location_1.longitude, location_1.latitude)
    dest_node = ox.nearest_nodes(graph, location_2.longitude, location_2.latitude)

    # Calculate the shortest path between the nodes
    route = ox.shortest_path(graph, orig_node, dest_node, weight='length')

    print(route)

    # Plot the route
    fig, ax = ox.plot_graph_route(graph, route, node_size=0)
    return fig, ax


# Find the route and display the plot
start = datetime.datetime.now()
print(start)
fig, ax = get_route(address_1, address_2)
end = datetime.datetime.now()
print(end)

