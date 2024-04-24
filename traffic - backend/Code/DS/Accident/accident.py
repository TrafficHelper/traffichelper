from itertools import product

from Code.DS.Accident.outcome import Outcome
from Code.DS.Atomic.vehicle import Vehicle
from Code.DS.environment import Environment, Surface, Visibility, Weather
# from Code.DS.Structural.section import Section
from Code.DS.Temporal.time import Time
from Code.Interfaces.parser import Parser
from Code.filenames import Filenames


class Accident(Parser): # TODO Re-include Section and associated methods after fixing it
    """
    Class representing each individual accident,
    - location: Location in Network Component (Edge: Road OR Node: Intersection)
    - time: Time interval of accident occurring
    - weather: Weather Type
    - outcome: The list of accident levels experienced by each vehicle type
    """

    def __init__(self, start: Time = None, end: Time = None, environment: Environment = None, outcome: Outcome = None):
        # self.location = location
        # Start and end times are the same when loading accidents from the data
        self.start = start
        self.end = end
        self.environment = environment
        self.outcome = outcome

    def parse(self, filename, data):
        fn = Filenames.collisiondata()
        env = Environment.grading(Environment.score(Surface.UNKNOWN.parse(fn, data), Weather.UNKNOWN.parse(fn, data), Visibility.UNKNOWN.parse(fn, data)))  # Get environment as combination of surface, weather and visibility
        out = Outcome()
        out.parse(filename, data)  # Get result of parsing data from filename
        occ = Time().parse(Filenames.collisiondata(), data)  # Get time of occurrence as parsed from collision data and time
        # self.location = None
        self.start = occ
        self.end = occ
        self.environment = env
        self.outcome = out

    @staticmethod
    def STANDARD():
        """
        Returns the list of STANDARD unacceptable Accident which is considered by the application.
        Its goal is to minimize the chance for any of these occurring.
        Right now, it is simply the combinations of all outcomes involving a maximum of each type of less than 3 people, for all environments
        :return: The list of all STANDARD unacceptable Accident
        """
        accs = [] # List of accidents
        start = Time(); start.set(0)
        end = Time(); end.set(-1)
        env = [e for e in Environment] # The domain of all types in the environment
        veh = [e for e in Vehicle]; veh.remove(Vehicle.RATIOS) # List of all vehicles
        num = 3 # Maximal value of size of possible accidents
        result = [ele for ele in product(range(1, num + 1), repeat=len(veh))] # All possible combinations of outcomes
        for elem in env:
            for k in result:
                fin = Accident(start, end, elem, result[k])
                accs.append(fin)
        return accs


    # def set(self, location: Section):
    #     self.location = location



