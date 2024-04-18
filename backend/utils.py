from code.helpers.enums import VehicleType, AccidentLevel, PERIOD
from code.ds.structures import Path, Graph, Node

class UserUtils:
    """
    Utility class representing the convenience methods accessible to any user.
    As these contain static methods, they do not need to be instantiated.
    """

    @staticmethod
    def computeRisk(vehicle:VehicleType, path:Path, intensity:AccidentLevel, left:int, right:int, period:int = PERIOD) -> float:
        """
        Compute the risk of an accident under the given parameters

        :param vehicle: The type of vehicle (ostensibly the user's vehicle choice)
        :param path: The path they have chosen to take, so compute the risk along the path
        :param intensity: The possible intensity of the accident
        :param left: The leftmost time modulo the period (they will simply enter a time and it will be converted this way)
        :param right: The rightmost time modulo the period (this will be computed by the application)
        :param period: Normally the basic period of the traffic to repeat itself, which is held over the entire network, though it may be smaller.
        :return: The chance of an accident under the given parameters
        """

        left%=period
        right%=period
        chance = 1
        for e in path.sequence: chance*=(1 - e.computeRisk(vehicle, intensity, left, right, period))
        return 1 - chance

    @staticmethod
    def minPath(vehicle:VehicleType, startTime:int, network:Graph, start:Node, end:Node, costVector:tuple[float] = (1, 0, 0)) -> Path:
        """
        Computes the minimal path optimizing a given set of parameters
        :param vehicle: The given vehicle type
        :param startTime: The given start time of the journey
        :param network: The graph network to optimize
        :param start: The starting node
        :param end: The ending node
        :param costVector: The cost of optimizing along each path. The first designates distance, the second, time, and the third, accidents
        :return: The minimal path optimizing the given set of parameters, or returns an empty path if no such path is possible
        """





