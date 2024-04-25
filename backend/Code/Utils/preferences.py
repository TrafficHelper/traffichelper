from DS.Accident.accident import Accident
from DS.Atomic.vehicle import Vehicle
from DS.environment import Environment
from Interfaces.cost import Cost


class Preferences:

    """
    Class representing the set of User Preferences
    The user preferences consist of:
    - Vehicle type
    - Environment
    - Accident tolerance
    - Cost metric: The cost metric is a triple weighted on (safety, distance, time) respectively
    """

    def __init__(self, vehicle:Vehicle, environment:Environment, tolerance:Accident, metric:Cost):
        self.vehicle = vehicle
        self.environment = environment
        self.tolerance = tolerance
        self.metric = metric





