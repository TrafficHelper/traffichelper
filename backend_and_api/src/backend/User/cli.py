import datetime
import osmnx

from backend.Code import loader
from backend.Constants import constants
from backend.Code.Accident.environment import Environment
from backend.Code.Atomic.gadget import Gadget
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Utils.preferences import Preferences
from backend.Code.Utils.utils import Utils
from backend.Code.mutation import Mutation
from backend.Code.user import User

class CLI:

    def __init__(self):
        """
        Creates a CLI instance for the session.
        Consists of a default user and associated default unique toolset for that user
        Based off the UNIX/LINUX zsh [7] shell
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
        """
        :param command: The command in str format
        :return: Executes an inputted tentative CLI command in a failsafe manner, catching any error
        """
        # Default error message if a command could not be interpreted - the following are the only potential answers in the first case
        error_msg = 'Command not recognized! Perhaps it was incorrect formatting or exceeding privileges.'
        try:
            components = command.split(' ')
            action = components[0] # The first section which designates the action
            # The universal terms used to refer to if a user wants to enter a node or an edge
            node_key = 'node'
            edge_key = 'edge'

            # Manual
            man_command = 'man'
            if action == man_command:
                for line in open(constants.CLI_INFO_FILEPATH):
                    print(line) # Print each line separated by a new line in the file of the cli info

            # Exit from CLI
            exit_command = 'exit'
            if action == exit_command:
                exit() # Exit takes precedence over all else, so exit

            # User modification:

            save_command = 'save' # Save a traffic network to a filename
            set_command = 'change' # Set a given filename to the user's default traffic network

            # Save associated graph
            if action == save_command: # Save given graphML file as user's graph
                assert len(components) >= 2
                filename = components[1]
                osmnx.save_graphml(self.user.curr_network, filename)
            # Set associated graph
            if action == set_command: # Set given graphML file to user's graph
                assert len(components) >= 2
                filename = components[1]
                new_graph = loader.osmnx.load_graphml(filename)
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
                    assert self.user.is_admin
                    if components[-1] == graph_designation: # Nothing after show graph command, means we should only show that
                        nsz = 1 # Changed depending on how prominent intersections should be seen as
                        elw = 1 # Changed depending on how prominent segments should be seen as
                        osmnx.plot_graph(self.user.curr_network, node_size=nsz, edge_linewidth=elw)
                    else:
                        # Show all data with specified nearest node or edge - or taking precedence, the actual node/edge if it is already specified

                        instructions, address, node_or_edge = command.split("'") # Should consist of display graph, with address, either as graph tuple with no spaces or str
                        node_or_edge = node_or_edge.strip()
                        structure = self.to_graph_id(address, True if node_or_edge == node_key else False if node_or_edge == edge_key else None)
                        print(structure)
                        data = self.user.curr_network.nodes[structure] if node_or_edge == node_key else self.user.curr_network.edges[structure] if node_or_edge == edge_key else None
                        print(data)

            # Set new preferences
            preference_command = 'preference'
            if action == preference_command:
                assert len(components) == 4
                action, vehicle, environment, metric = components
                chosen_vehicle = Vehicle.for_name('Vehicle.'+vehicle) # The vehicle is parsed based on Vehicle.
                chosen_environment = Environment.forname(environment) # Environment is plainly parsed
                chosen_metric = tuple(float(e) for e in metric[1:-1].split(',')) # Metric must consist of braces containing numbers without any spaces
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

                tmp = after.strip().split(' ')
                add_or_rm = 'False' if len(tmp) < 5 else tmp[4] # Redundant failsafe parameter as user probably wants to refactor flows if they're adding or removing network edge
                node_or_edge, added, removed, refactor = (tmp[0], tmp[1], tmp[2], tmp[3])
                parse_bool = lambda inp: True if inp == 'True' else False if inp == 'False' else None # Helpful for interpreting boolean str to actual bool
                # lat, long = osmnx.geocode(location)
                # location = osmnx.nearest_nodes(self.user.curr_network, long, lat) if node_or_edge == 'node' else osmnx.nearest_edges(self.user.curr_network, long, lat) if node_or_edge == 'edge' else None
                ab = [] if len(added) == 2 else [Gadget.for_name(gad) for gad in added[1:-1].split(',')]
                cd = [] if len(removed) == 2 else [Gadget.for_name(gad) for gad in removed[1:-1].split(',')]
                refactor = parse_bool(refactor)
                location = self.to_graph_id(location, True if node_or_edge == node_key else False if node_or_edge == edge_key else None)
                # Create mutation from parsed location, added & removed gadgets and whether to refactor, and apply it
                change = Mutation(self.user.curr_network, location, ab, cd, parse_bool(add_or_rm))
                print('Cost:' + str(change.cost()))
                self.tools.apply([(change, refactor)])
        except FileNotFoundError: # TODO Fix Assertion Error
            print(error_msg) # Print error message in some error happened - the error message covers all possible contingencies

    def to_graph_id(self, inp:str, node_or_edge:bool):

        """
        Converts the string input, which must either be an address, coordinate or edge or node id, to an edge or node id
        :param inp: str designating the input
        :param node_or_edge: bool: True --> node, False --> edge. Used to resolve ambiguity
        :return: Convert input to satisfying graph structure for user using edge or node as guidance
        """

        # Convert coordinate to closest node or edge, depending on user's choice
        feature = lambda lt, lg, noe: osmnx.nearest_nodes(self.user.curr_network, lg, lt) if noe else osmnx.nearest_edges(self.user.curr_network, lg, lt)
        # HAS --> If valid, HAS to obey criterion
        if inp[0] == '(' and inp[-1] == ')':  # Tuple has first and last chars as opening and closing braces
            elements = inp[1:-1].split(',') # Remove comma and get all elements
            if len(elements) == 3: # HAS to be edge structure with all elements integers
                print(True)
                return tuple(int(elm) for elm in elements)
            if len(elements) == 2: # HAS to be coordinate pair; nodes are unique identifiers
                return feature(float(elements[0]), float(elements[1]), node_or_edge)
            if len(elements) == 1: # HAS to be unique nodeID, in which case node_or_edge is OVERRIDDEN for returning edge
                return int(elements[0])
            else:
                raise ValueError('Invalid argument parsed')
        else: # HAS to be an address
            lat, lng = osmnx.geocode(inp)
            return feature(lat, lng, node_or_edge)

# TESTING CODE
# if __name__ == '__main__':
#     act = CLI()
#     print(act.to_graph_id('4 Sheldrake Drive, Kanata, Ottawa', True))
#     print(act.to_graph_id('4 Sheldrake Drive, Kanata, Ottawa', False))
#     print(act.to_graph_id('(45.3451,-75.32143)', True))
#     print(act.to_graph_id('(45.3451, -75.32143)', False))
#     print(act.to_graph_id('(899581512)', True))
#     print(act.to_graph_id('(899581512)', False))
#     print(act.to_graph_id('(11896701208, 11896701208, 1)', True))
#     print(act.to_graph_id('(11896701208, 11896701208, 1)', False))
#     print(act.to_graph_id('(23432, 32423)', True))
#     print(act.to_graph_id('(23432, 32423)', False))






