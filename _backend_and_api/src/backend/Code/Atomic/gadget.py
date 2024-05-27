from __future__ import annotations

import datetime
from enum import Enum

from backend.Code.Interfaces.cost import Cost
from backend.Code.Interfaces.parser import Parser


class Gadget(Cost, Parser, Enum):

    """
    Enum of all traffic Gadget considered in the application
    All traffic features which can be edited, except for adding/removing an Edge
    """

    # List of Gadgets

    LANE = 1 # A road segment will have a given number of these lanes added to it
    SPEED_INCREASE = 2 # The maximum speed of the road is 5 x the number of such gadgets it has
    STOP_LIGHT = 3 # Whether this edge or intersection possesses a stop light to control fast traffic
    SPEED_ENFORCER = 4 # Whether this edge or intersection penalizes vehicles for disobeying the rules

    DISCRETION = 5 # The difference, in kph, adding a successive speed limit chunk is worth

    def cost(self):
        """
        Returns the cost of each of the gadgets, i.e. how much it costs to implement them.
        Will always add it to a fixed APPROVAL COST
        :return: The cost of each gadget
        """

        approval_cost = 150 # https://www.ola.org/sites/default/files/common/how-bills-become-law-en.pdf (ontario bill but practically the same)
        match self.value:
            # Averages from ...
            case Gadget.SPEED_INCREASE.value: return approval_cost
            case Gadget.LANE.value: return approval_cost+10**6
            case Gadget.SPEED_ENFORCER.value: return approval_cost+4327 # https://www.cbc.ca/news/canada/ottawa/annoying-thing-speed-cameras-ottawa-they-work-1.6786951
            case Gadget.STOP_LIGHT.value: return approval_cost+4375 # https://www.toronto.ca/services-payments/streets-parking-transportation/traffic-management/traffic-signals-street-signs/traffic-signals-in-toronto/traffic-signal-installation/
            case _: raise ValueError("Invalid Gadget type")

    @staticmethod
    def expense(system:{Gadget:(int, float)}, start:datetime.datetime, end:datetime.datetime):
        """
        Computes the total expense of the system of Gadgets, frequencies and costs, adjusted for given time
        The expense is a weighted sum of the frequencies and individual costs times a normalizing factor for time
        :param system: The Gadget, frequency and Cost groupings
        :param start: The time period start measured over
        :param end: The time period end measured over
        :return: The total expense of the system over the given time
        """
        return (end - start)*sum(feature[0]*feature[1] for feature in system) # Weighted sum of number of Gadget times expense for all Gadget

    def parse(self, filename:str, data):
        """
        IN THIS CASE WE ASSUME THE FILENAME DESIGNATES THE GADGET ITSELF
        THIS PARSE METHOD IS SOLELY CALLED BY THE WEB INTERFACE
        :param filename:
        :param data:
        :return:
        """
        match filename:
            case 'LANE': return Gadget.LANE
            case 'SPEED_INCREASE': return Gadget.SPEED_INCREASE
            case 'STOP_LIGHT': return Gadget.STOP_LIGHT
            case 'SPEED_ENFORCER': return Gadget.SPEED_ENFORCER
            case _: raise ValueError('Invalid gadget name')

    @staticmethod
    def for_name(gad_name):
        """
        :param gad_name: The str name of the object
        :return: The Gadget obj based on OSMnx serialized GraphML str name
        """
        return {'Gadget.LANE': Gadget.LANE, 'Gadget.SPEED_INCREASE':Gadget.SPEED_INCREASE, 'Gadget.STOP_LIGHT':Gadget.STOP_LIGHT, 'Gadget.SPEED_ENFORCER':Gadget.SPEED_ENFORCER}[gad_name]




