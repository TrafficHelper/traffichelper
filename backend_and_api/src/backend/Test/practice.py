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