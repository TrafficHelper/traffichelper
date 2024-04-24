from DS.Accident.injury import Injury
from DS.Atomic.vehicle import Vehicle
from Interfaces.parser import Parser
from filenames import Filenames


class Outcome(Parser):

    """
    Represents the potential possibilities for an accident to occur
    There isn't any range of possibilities as multi-car pileups, for example, are uncommon
    """

    def __init__(self, outcome: {Vehicle: [Injury]} = None):
        """
        Outcome consists of a dict of vehicle types (including pedestrians) and the outcome to each of them
        The (length of the) list associated with each vehicle designates the number of such vehicles
        It is too complex to determine the positioning and model the spatial dynamics of the participants which would provide a better analysis.
        :param outcome:
        """
        self.outcome = outcome

    def grading(self, level:Injury):
        return {vehicle:self.outcome[vehicle].count(level) for vehicle in self.outcome} # Return grouping of vehicles with level of Injury

    def involved(self):
        return sum([len(self.outcome[vehicle]) for vehicle in self.outcome]) # Number of vehicles completely involved

    def __str__(self):
        return str(self.outcome)

    def parse(self, filename, data):

        """
        Parses the given outcome from the data, the filename being TrafficCollisionData.csv
        Uses the parameter self as the outcome to attach data to
        It first parses the injury levels, then the involved vehicles, and then assigns the vehicles to injury levels
        The highest injury levels are assigned to the "weakest" Vehicles first, in the given ordering, working backwards until no injury is reached
        This approximation process is reasonable, and cannot be made any better, as there is no extra information contained in this or any other file.
        :param filename: TrafficCollisionData.csv; the file name from which it is being parsed, redundant parameter otherwise
        :param data: The data line from the filename
        :return: An Outcome, or assignment of Vehicles to list of Injuries
        """

        # Range(filename) = TrafficCollisionData.csv

        url = Filenames.collisiondata()
        vehicles = Vehicle.CAR.parse(url, data)  # List of vehicles, including pedestrians from most to least vulnerable
        value, injuries = Injury.UNINJURED.parse(url, data)  # Injuries from largest to smallest; if value is true, then no other injuries except to "weakest" vehicle

        outcomes = {conveyance:[Injury.UNINJURED]*vehicles[conveyance] for conveyance in vehicles}

        # print(value)
        # print(vehicles)
        # print(injuries)
        # print(outcomes)

        if not value: # If the maximal damage is P.D. only, all others are zero
            outcomes[Vehicle.CAR if len(outcomes[Vehicle.MOTORCYCLE]) == 0 else Vehicle.MOTORCYCLE][0] = Injury.MINIMAL
            self.outcome = outcomes
            return

        # Strategy; work backwards, iterating over injuries in decreasing order

        inji = 0 # The current index of the injury in decreasing intensity
        harms = list(injuries.keys()) # List of all injury keys
        sub = 0 # The number of injuries of the sub, level corresponding to harms[inji]

        for vehicle in outcomes: # Iterate over each vehicle from most to least vulnerable
            for number in range(len(outcomes[vehicle])): # For each of the possible vehicles to fill with injuries
                if inji == len(harms): # Run out of injuries; some vehicles' status is ambiguous
                    break
                current = harms[inji] # The current injury
                outcomes[vehicle][number] = current
                sub+=1
                if sub == injuries[current]+1:
                    inji+=1
                    sub = 0

        # Strategy:
        # Assign each vehicle with a level of injury;We will assume Pedestrian < Bicycles < Motorcycles < Cars < Trucks in the damage hierarchy
        # Vehicles are ordered by fragility with Pedestrian < Bicycles < Motorcycles < Cars < Trucks
        # For intensity of injuries move from right to left, move with targets from left to right and fill up all amounts before moving on
        # There cannot be more injuries than vehicles but if P.D. only exists and no structure has had an injury, arbitrarily move the smallest filled on to it

        # Basic outcome consists of conveyance of all assumed uninjured vehicles
        self.outcome = outcomes
