import numpy


class Cost:

    """
    Interface Cost
    Used as a common interface to represent the quantitative cost of some action. It is used in a variety of contexts
    Each type using it extends from this Cost class and overrides the cost(self) method
    """

    STANDARD = (1/3, 1/3, 1/3) # The default cost (involving an equal balance between each method)

    def cost(self) -> float:
        """
        Main method of Cost interface
        Ostensibly consists of a linear function time, distance and safety, respectively, returning the cost of a Segment or Intersection
        Whether to change this evaluation is dependent on the overrider and is the reason there are no predefined parameters
        :return: Overridden to return a float designating the cost of the self
        """
        pass



