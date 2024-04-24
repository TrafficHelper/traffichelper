from Code.DS.Accident.accident import Accident
from Code.DS.Atomic.vehicle import Vehicle
from Code.DS.Structural.graph import Graph
from Code.DS.Structural.statistic import Statistic
from Code.DS.environment import Environment
from Code.Utils.preferences import Preferences
from Code.filenames import Filenames


class Loader:

    @staticmethod
    def load():
        """
        Loads all parsed data into the Graph representing the traffic network
        :return: Graph representing all parsed data
        """

        # Load network structure
        network = Graph()
        network.parse(Filenames.centrelines(), [])
        print('DONE')
        print(network.nodes)

        # Create user preferences
        prefs = Preferences(Vehicle.CAR, Environment.NORMAL, Accident.STANDARD())




