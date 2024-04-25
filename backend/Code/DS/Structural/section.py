import random

from DS.Atomic.gadget import Gadget
from DS.Structural.statistic import Statistic
from Interfaces.cost import Cost


class Section(Cost):
    """
    A Section represents a section of a traffic network, as either a Node(road) or Edge(intersection)
    The Section class unifies all common properties between the two, and consists of:
    - Statistic
    - Gadget
    - name
    """

    def __init__(self, stats: Statistic, gadgets: [Gadget], name: str = '', length:float = 30):
        self.stats = stats
        self.gadgets = gadgets
        self.name = name
        self.length = length # This designates the length of the section; It must have nonzero size, so it is set to default intersection size of 30m

    def __str__(self):
        return 'Section['+str(self.stats)+', '+str(self.gadgets)+', '+self.name+', '+str(self.length)+']'

    def modify(self, feature: Gadget, op: bool = True, preserve:bool = False):
        """
       Modifies a non None Gadget on this Segment
       op:bool[True|False] --> [Add|Remove]
       :param feature: The feature to modify with respect to the segment
       :param op: Whether to Add or Remove the feature Gadget from this Section
       :param preserve: Whether to simply add or remove the gadgets or also to compute changes to the network
       :return: [True|False] --> [Successful completion|Unsuccessful, ex. removable Gadget not with Section]
        """

        # Disclaimer: This function is merely an approximation and is as accurate as the data and methodology

        self.gadgets.append(feature)
        self.gadgets.remove(feature)
        if preserve: # Simple modification; but by default we compute changes
            return
        c = self.stats.accidents
        random.shuffle(c)
        est = 0 # The estimated proportion of accidents removed by a feature
        change = 0 # The change (decrease) in speed wrought by a feature
        if feature == Gadget.ENFORCER: # Automated Speed Camera
            est = int(len(c)*0.20) # estimate from https://www.sciencedirect.com/science/article/pii/S0001457524000708
            # Traffic volumes don't change but speeds decrease by ~ 11 km/h = 184 m/min --> times increase
            change = 0.184 # set new time

        elif feature == Gadget.CROSSOVER: # Crosswalk
            est = int(len(c)*0.25) # estimate from https://rosap.ntl.bts.gov/dot/dot_16378_DS1.pdf
            change = 0.067 # estimate from https://www.fhwa.dot.gov/publications/research/safety/00101/00101.pdf

        elif feature == Gadget.STOPLIGHT: # Traffic Light
            est = int(len(c)*0.11) # estimate from https://uknowledge.uky.edu/cgi/viewcontent.cgi?article=1064&context=ktc_researchreports
            change = 0.009 # estimate from https://www.reddit.com/r/cycling/comments/ji4e2j/how_much_do_stoplights_actually_slow_down_a_ride/

        elif feature == Gadget.CAMERA: # Red-Light camera
            est = int(len(c)*0.20) # estimate from https://www.tslawyers.ca/blog/personal-injury/red-light-cameras-reduce-angle-collisions-in-eastern-ontario/
            change = 0.024
        if op:
            # TODO Decide whether +1 to round up works here...
            self.stats.accidents = c[est:] # Refactor times to account for ADDING Gadget
        else: # Increase accidents in reverse to account for REMOVING Gadget
            ax = self.stats.accidents
            for elem in self.stats.accidents[:est]:
                ax.append(elem)
            self.stats.accidents = ax
        self.stats.tempest(self.length,0.833 + (-1 if op else 1)*change) # Times taken should increase due to such impediments

    def cost(self):
        """
        Return the time-independent PARTIAL Cost of this Section
        The Cost is the sum of the Section (given its length and tarmac rate), and the sum of the individual gadgets on it
        :return: The time-independent PARTIAL Cost of this Section
        """
        rate = 2500 # Cost of average Urban Road Segment per meter: https://blog.midwestind.com/cost-of-building-road/
        return self.length*rate + sum(g.cost() for g in self.gadgets)
