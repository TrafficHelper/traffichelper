import numpy


class Cost:

    """
    Interface Cost
    Used as a common interface to represent the quantitative cost of some action. It is used in a variety of contexts
    Each type using it extends from this Cost class and overrides the cost(self) method
    """

    DEFAULT = lambda metric: numpy.dot((1, 1, 1), metric) # The default cost (involving maximizing emphasis on safety, distance and time)

    def cost(self) -> float:
        """
        Main method of Cost interface
        Ostensibly consists of a linear function time, distance and safety, respectively, returning the cost of a Segment or Intersection
        Whether to change this evaluation is dependent on the overrider and is the reason there are no predefined parameters
        :return: Overridden to return a float designating the cost of the self
        """
        pass

class Impl(Cost):
    def cost(self):
        return 1

if __name__ =='__main__':
    res = Impl().cost()
    print(res)



