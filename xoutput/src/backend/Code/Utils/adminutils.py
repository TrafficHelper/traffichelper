# import Gadget
# from Code.DS.Mutation.modification import Modification
# from Code.DS.Structural.graph import Edge
# from Code.Interfaces.cost import Cost
# from Code.Utils.utils import Utils
#
#
# class AdminUtils(Utils):
#
#     """
#     A class representing all actions possible to conduct ONLY by administrators.
#     An administrator has superuser privileges, being able to do all the user method available in the Utils class too.
#
#
#
#     """
#
#     def alterations(self, budget:int, gadgets:[Gadget], cost:Cost) -> Modification:
#         """
#         Returns the series of Modifications such that:
#          - All Actions of the Modifications are in the permissible Gadget
#          - The expense of the Modifications is below the budget
#          - The Graph, after applying the Modifications, has the lowest value measured by the Cost parameter
#         \nAdditionally, if one wants to restrict the modifications to particular locations, they can re-instantiate the Graph with the requisite features trimmed, and recall the function
#         :param budget: The budget of the modifications
#         :param gadgets: The constraints on the list of Gadgets permissible in the Modifications
#         :param cost: The Cost metric to measure the total new cost of the network
#         :return:
#         """
#
#    # def bestmodify(self, budget:int, gadgets:[Gadget], locations:[Edge], cost:Cost) -> Modifications:
#    #     """
#    #     Return the best Modification Sequence to apply to the (implicitly declared) network to minimize cost while remaining in budget
#    #     This is NP-Hard; even finding a sum of budgets as close as possible to the given budget limit limits the potential benefit.
#    #     For this reason, AIML is used to provide an appproximate solution to the problem
#    #     Each addition and removal of a road provides a measured difference to the cost (AIML)
#    #     Each addition and removal of a gadget on the road also provides a measurable difference (AIML)
#    #     From the current change of zero, the maximum negative value is desired. Choosing the greatest of each of these costs determines it.
#    #     We can determine, using the Knapsack problem DP algo as a consequence as well.
#    #
#    #     :param budget:
#    #     :return:
#    #     """
#    #
#    #     self.network.refactor(locations)
