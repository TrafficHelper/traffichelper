import datetime

import networkx
import osmnx

from backend.Code.Accident.environment import Environment
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Utils.preferences import Preferences
from backend.Code.Utils.utils import Utils
from backend.Code.user import User

class CLI:

    exit_command = 'exit'

    def __init__(self):
        self.user = User()
        self.tools = Utils(self.user)

    def repl(self):
        while True:
            command = input('>>: ')
            self.execute_command(command)

    def execute_command(self, command):
        error_msg = 'Command not recognized! Perhaps it was incorrect formatting or exceeding privileges.'
        recognized = False
        try:
            components = command.split(' ')

            action = components[0] # The first section

            exit_command = 'exit'
            if action == exit_command:
                recognized = True
                assert len(components) == 1 # Only exit command
                exit()

            # User modification:

            save_command = 'save' # Save a traffic network to a filename
            set_command = 'set' # Set a given filename to the user's default traffic network

            if action == save_command: # Save given graphML file
                assert len(components) == 2
                recognized = True
                target = components[1]
                osmnx.save_graphml(self.user.curr_network, target)
            if action == set_command: # Set given graphML file
                assert len(components) == 2
                recognized = True
                target = components[1]
                new_graph = osmnx.load_graphml(target)
                self.user = User(new_graph, self.user.is_admin)

            sudo_command = 'sudo'
            if action == sudo_command:
                assert len(components) == 1
                recognized = True
                self.user.make_admin()

            display_command = 'display'
            if action == display_command:

                target = components[1]

                recognized = True
                print(target)
                if target == 'user':
                    print(self.user)
                if target == 'graph':
                    if components[-1] == 'graph':
                        osmnx.plot_graph(self.user.curr_network, node_size=3)
                    else:
                        # Get edge/node properties along that edge
                        instructions, address, concl = command.split("'")
                        plc = osmnx.geocode(address) # Remove start and end quotes
                        print(concl)
                        key = True if concl[1:] == 'edge' else False
                        nearest = osmnx.nearest_nodes(self.user.curr_network, plc[1], plc[0]) if not key else osmnx.nearest_edges(self.user.curr_network, plc[1], plc[0])
                        print(nearest)
                        attrs = self.user.curr_network.nodes[nearest] if not key else self.user.curr_network.edges[nearest]
                        print(attrs)

            preference_command = 'preference'
            if action == preference_command:
                assert len(components) == 4
                recognized = True
                vehicle, environment, metric = (components[pos] for pos in [1, 2, 3])
                chosen_vehicle = Vehicle.for_name('Vehicle.'+vehicle)
                chosen_environment = Environment.forName(environment)
                chosen_metric = tuple(float(e) for e in metric[1:-1].split(','))
                assert len(chosen_metric) == 3 # Can only account for three parameters
                self.user.preferences = Preferences(chosen_vehicle, chosen_environment, chosen_metric)

            optimal_command = 'optimal'
            if action == optimal_command:
                action, start_address, redundant, end_address, num_paths = command.split("'")
                start_point = osmnx.geocode(start_address)
                end_point = osmnx.geocode(end_address)
                best_paths = self.tools.optimal_paths(datetime.datetime.now(), start_point, end_point, int(num_paths))
                recognized = True
                print(self.tools.paths_coordinates(best_paths))
                print(self.tools.paths_names(best_paths))
                self.tools.print_paths(best_paths)

        except AssertionError:
            print(error_msg)
            pass

        print(error_msg if not recognized else '')
