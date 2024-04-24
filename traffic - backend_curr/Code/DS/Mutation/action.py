from DS.Atomic.gadget import Gadget
from DS.Structural.graph import Node, Edge
from DS.Structural.section import Section
from Interfaces.cost import Cost


class Action(Cost):

    """
    An Action consists of an atomic change on a Section or Gadget, either through its addition or removal
    Bundled together, a series of Actions form a Modifications
    """

    def __init__(self, change:bool, section:Edge, gadget:Gadget = None):
        self.directive = change # change: [True, False] --> [Add, Remove]
        self.section = section # Node|Edge to operate on
        self.gadget = gadget # gadget:[Gadget, None] --> directive on [gadget, section]

    def cost(self):
        """
        Returns the total Cost of the Action.
        The total Cost is the sum of the Gadgets inv
        :return:
        """
        if self.directive: # Add something
            return self.section.cost() if self.gadget is None else self.gadget.cost()
        else: # Remove something
            # Estimate 0.01 of installation cost to remove Tarmac and 0.05 of installation cost to remove Gadget
            return 0.1*self.section.cost() if self.gadget is None else 0.05*self.gadget.cost()

    def apply(self, left:Node, right:Node):
        if self.gadget is not None:
            self.section.modify(self.gadget, self.directive)
        # If Section is lone, we are forced to leave it alone
        # In both cases we assume that adding or removing a single Edge to the network does not change its composition
        # TODO Fix this paradigm
        if self.directive:
            self.section.outgoing = left
            self.section.incoming = right
        else:
            self.section.rstar(Node(None, None))
            self.section.rend(Node(None, None))

