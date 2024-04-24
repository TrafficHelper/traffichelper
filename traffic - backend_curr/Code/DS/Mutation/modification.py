from DS.Mutation.action import Action
from DS.Structural.graph import Graph
from Interfaces.cost import Cost


class Modification(Cost):

    """
    Modifications consist of a series of Actions applied to a Graph
    """

    def __init__(self, target:Graph):
        self.objective = target
        self.modifications = []
        self.expense = 0

    def __add__(self, other:Action):
        self.modifications+=other
        self.expense+=other.cost()

    def __sub__(self, other:Action):
        if other not in self.modifications:
            return None
        self.modifications.remove(other)
        self.expense-=other.cost()
        return other

    def cost(self):
        """
        Return the Cost of this Modification
        :return: The Cost of this Modification
        """
        return self.expense

    def execute(self) -> [bool]:
        """
        Executes the Modification as a series of Actions
        Returns a trace on which modifications were possible
        Uses a greedy strategy when conducting actions; it is moved from left to right and skipping impossible actions
        Thus had the actions been conducted in a different order, it would produce a different result
        :param:preserve
        :return: The result of the Modification
        """
        n = len(self.modifications)
        trace = [False]*n
        for j in range(n): # Perform an action
            action = self.modifications[j]
            result = action.execute()
            if result:
                trace[j] = True
        return trace
