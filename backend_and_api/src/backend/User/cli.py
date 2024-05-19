import datetime
import osmnx


from Code.Accident.environment import Environment
from Code.Atomic.vehicle import Vehicle
from Code.Utils.preferences import Preferences
from Code.Utils.utils import Utils
from Code.user import User

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
                assert len(components) == 2

                target = components[1]

                recognized = True
                print(target)
                if target == 'user':
                    print(self.user)
                if target == 'graph':
                    osmnx.plot_graph(self.user.curr_network)

            preference_command = 'preference'
            if action == preference_command:
                assert len(components) == 4
                recognized = True
                vehicle, environment, metric = (components[pos] for pos in [1, 2, 3])
                chosen_vehicle = Vehicle.OTHER
                chosen_vehicle = Vehicle.for_name(vehicle)
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
                print(best_paths)
                # print(self.tools.beautify(best_paths))
                print(self.tools.paths_coordinates(best_paths)) # Returns the paths with their nodeID sequence replaced with coordinate sequence
                self.tools.print_paths(best_paths)
        except AssertionError:
            pass

        print('Command not recognized' if not recognized else '')
