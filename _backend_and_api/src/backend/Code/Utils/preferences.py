from backend.Code.Accident.accident import Accident
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Accident.environment import Environment
from backend.Code.Interfaces.cost import Cost


class Preferences:

    """
    Class representing the set of User Preferences
    These are an integral part of the user's
    The user preferences consist of:
    - Vehicle type
    - Environment
    - Accident intolerance, which lists all accidents that the user doesn't want considered
    - Cost metric: The cost metric is a triple weighted on (safety, distance, time) respectively
    """

    def __init__(self, vehicle: Vehicle = Vehicle.CAR, environment: Environment = Environment.NORMAL, metric:(float, float, float) = Cost.STANDARD, intolerance: [Accident] = []):
        self.vehicle = vehicle
        self.environment = environment
        self.intolerance = intolerance
        self.metric = metric

    def __str__(self):
        return '[Vehicle: '+str(self.vehicle) + ', Environment: ' + str(self.environment) + ', Metric: '+str(self.metric) + ']'








