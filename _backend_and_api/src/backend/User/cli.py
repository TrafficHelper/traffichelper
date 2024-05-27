import datetime
import osmnx

from backend.Code.Accident.environment import Environment
from backend.Code.Atomic.gadget import Gadget
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Utils.preferences import Preferences
from backend.Code.Utils.utils import Utils
from backend.Code.mutation import Mutation
from backend.Code.user import User

class CLI:

    # Changed depending on what the unique admin password is.

    def __init__(self):
        """
        Creates a CLI instance for the session.
        Consists of a default user and associated default unique toolset for that user
        """
        self.user = User()
        self.tools = Utils(self.user)

    def repl(self):
        """
        repl --> Read-Eval-Print-Loop
        Repeatedly enters the input until the exit command is clicked
        """
        while True:
            command = input('>>: ')
            self.execute_command(command)

    def execute_command(self, command):
        # Default error message if a command could not be interpreted - the following are the only potential answers in the first case
        error_msg = 'Command not recognized! Perhaps it was incorrect formatting or exceeding privileges.'
        try:
            components = command.split(' ')
            action = components[0] # The first section which designates the action

            # Exit from CLI
            exit_command = 'exit'
            if action == exit_command:
                exit() # Exit takes precedence over all else, so exit

            # User modification:

            save_command = 'save' # Save a traffic network to a filename
            set_command = 'set' # Set a given filename to the user's default traffic network

            # Save associated graph
            if action == save_command: # Save given graphML file
                assert len(components) >= 2
                filename = components[1]
                osmnx.save_graphml(self.user.curr_network, filename)
            # Set associated graph
            if action == set_command: # Set given graphML file to user's graph
                assert len(components) >= 2
                filename = components[1]
                new_graph = osmnx.load_graphml(filename)
                self.user = User(new_graph, self.user.is_admin)

            pass_key = 'testkey'
            sudo_command = 'sudo' # Make admin
            if action == sudo_command:
                assert len(components) >= 2
                if components[1] == pass_key:
                    self.user.make_admin()
                    print('Successful admin logon')
                else:
                    print('Unsuccessful logon, please retry command')

            display_command = 'display'
            if action == display_command:
                assert len(components) >= 2
                target = components[1]

                user_designation = 'user' # What a user is parsed from
                if target == user_designation: # Want to show user preferences
                    print(self.user)

                graph_designation = 'graph'
                if target == graph_designation: # What a graph is parsed from
                    if components[-1] == graph_designation: # Nothing after show graph command, means we should only show that
                        nsz = 1 # Changed depending on how prominent intersections should be seen as
                        elw = 1 # Changed depending on how prominent segments should be seen as
                        osmnx.plot_graph(self.user.curr_network, node_size=nsz, edge_linewidth=elw)
                    else:
                        # Show all data with specified nearest node or edge - or taking precedence, the actual node/edge if it is already specified

                        instructions, address, node_or_edge = command.split("'") # Should consist of display graph, with address, either as graph tuple with no spaces or str
                        node_or_edge = node_or_edge.strip()
                        print(instructions, address, node_or_edge)
                        node_key = 'node'
                        edge_key = 'edge'
                        place = None
                        # ONLY ATTEMPT TUPLE IF YOU KNOW TO SEARCH IT ON GRAPH
                        if address[0] == '(' and address[-1] == ')': # Probably tuple here
                            # Parse tuple in three integer parts - it must not be space-separated
                            place = tuple(int(des) for des in address[1:-1].split(',')) # u, v, key
                        else: # Find nearest section along address under specified code
                            lat, long = osmnx.geocode(address)
                            place = osmnx.nearest_nodes(self.user.curr_network, long, lat) if node_or_edge == node_key else osmnx.nearest_edges(self.user.curr_network, long, lat) if node_or_edge == edge_key else None
                        print(place)
                        unknown_msg = 'Specified node or edge is not contained in the graph' # Called if user's specified node or edge not in graph
                        if node_or_edge == node_key:
                            node_list = self.user.curr_network.nodes # node:data dict of nodes and data
                            if place not in node_list:
                                print(unknown_msg)
                            else:
                                print(node_list[place])
                        if node_or_edge == edge_key:
                            edge_list = self.user.curr_network.edges
                            if place not in edge_list:
                                print(unknown_msg)
                            else:
                                print(edge_list[place])
                        else:
                            print('Unspecified closest node or edge')

                # if target == 'graph':
                #     if components[-1] == 'graph':
                #         osmnx.plot_graph(self.user.curr_network, node_size=3)
                #     else: # Show stats for particular edge closest to location
                #         # Get edge/node properties along that edge
                #         instructions, address, concl = command.split("'")
                #         plc = osmnx.geocode(address) # Remove start and end quotes
                #         key = True if concl[1:] == 'edge' else False
                #         nearest = osmnx.nearest_nodes(self.user.curr_network, plc[1], plc[0]) if not key else osmnx.nearest_edges(self.user.curr_network, plc[1], plc[0])
                #         print(nearest)
                #         attrs = self.user.curr_network.nodes[nearest] if not key else self.user.curr_network.edges[nearest]
                #         print(attrs)

            # Set new preferences
            preference_command = 'preference'
            if action == preference_command:
                assert len(components) == 4
                action, vehicle, environment, metric = components
                chosen_vehicle = Vehicle.for_name('Vehicle.'+vehicle) # The vehicle is parsed based on Vehicle.
                chosen_environment = Environment.forName(environment) # Environment is plainly parsed
                chosen_metric = (float(e) for e in metric[1:-1].split(',')) # Metric must consist of braces containing numbers without any spaces
                assert len(chosen_metric) == 3 # Metric must contain only three parameters
                self.user.preferences = Preferences(chosen_vehicle, chosen_environment, chosen_metric) # Set preferences to new

            # Get optimal paths
            optimal_command = 'optimal'
            if action == optimal_command:
                # Action is 'optimal', redundant is empty space, num_paths is of type float
                action, start_address, redundant, end_address, num_paths = command.split("'")
                start_point = osmnx.geocode(start_address)
                end_point = osmnx.geocode(end_address)
                best_paths = self.tools.optimal_paths(datetime.datetime.now(), start_point, end_point, int(num_paths))
                print(self.tools.paths_coordinates(best_paths))
                print(self.tools.paths_names(best_paths))
                self.tools.print_paths(best_paths)

            # Modify Graph network
            modify_command = 'modify'
            if action == modify_command:

                assert self.user.is_admin # Only admin can modify
                before, location, after = command.split("'")
                node_or_edge, added, removed, refactor = after.strip().split(' ')
                lat, long = osmnx.geocode(location)
                location = osmnx.nearest_nodes(self.user.curr_network, long, lat) if node_or_edge == 'node' else osmnx.nearest_edges(self.user.curr_network, long, lat) if node_or_edge == 'edge' else None
                ab = [] if len(added) == 2 else [Gadget.for_name(gad) for gad in added[1:-1].split(',')]
                cd = [] if len(removed) == 2 else [Gadget.for_name(gad) for gad in removed[1:-1].split(',')]
                refactor = bool(refactor)
                # Create mutation from parsed location, added & removed gadgets and whether to refactor, and apply it
                self.tools.apply([(Mutation(self.user.curr_network, location, ab, cd), refactor)])
                recognized = True
        except AssertionError:
            print(error_msg)
            pass

