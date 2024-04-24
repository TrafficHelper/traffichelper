from __future__ import annotations
from enum import Enum

from Code.DS.Temporal.time import Time
from Code.Interfaces.cost import Cost
from Code.Interfaces.parser import Parser
from Code.filenames import Filenames


class Gadget(Parser, Cost, Enum):

    """
    Enum of all traffic Gadget considered in the application
    All traffic features which can be edited, except for adding/removing an Edge
    """

    # List of Gadgets
    ENFORCER = 1 # Automated speed camera
    CROSSOVER = 2 # Crosswalk/Zebra Crossing
    STOPLIGHT = 3 # Traffic Light
    CAMERA = 4 # Red Light Camera

    def cost(self):
        """
        Return the cost of this single gadget per week (default recurrence time)
        Results were computed from online sources
        :return: The cost of this single gadget
        """
        match self.value:
            # Averages from ...
            case Gadget.ENFORCER.value: return 4327 # https://www.cbc.ca/news/canada/ottawa/annoying-thing-speed-cameras-ottawa-they-work-1.6786951
            case Gadget.CROSSOVER.value: return 1675 # http://guide.saferoutesinfo.org/engineering/marked_crosswalks.cfm
            case Gadget.STOPLIGHT.value: return 4375 # https://www.toronto.ca/services-payments/streets-parking-transportation/traffic-management/traffic-signals-street-signs/traffic-signals-in-toronto/traffic-signal-installation/
            case Gadget.CAMERA.value: return 1020 # https://getinvolved.cityofkingston.ca/red-light-camera/widgets/41523/faqs
            case _: raise ValueError("Invalid Gadget type")

    @staticmethod
    def expense(system:{Gadget:(int, float)}, time:float):
        """
        Computes the total expense of the system of Gadgets, frequencies and costs, adjusted for given time
        The expense is a weighted sum of the frequencies and individual costs times a normalizing factor for time
        :param system: The Gadget, frequency and Cost groupings
        :param time: The time period measured over
        :return: The total expense of the system over the given time
        """
        return time/Time.RECURRENCE*sum(feature[0]*feature[1] for feature in system) # Weighted sum of number of Gadget times expense for all Gadget

    def parse(self, fname, data):
        """
        Parses the Gadget from the data present in the filename and associates it with the
        So far, the filenames are:
        - AutomatedSpeedEnforcementCameraLocations.csv : ENFORCER
        - PedestrianCrossoverLocations.csv : CROSSOVER
        - ?: STOPLIGHT --> For now we assume that if the filename is empty, it denotes a stoplight
        - RedLightCameraLocations.csv : CAMERA
        :param fname: The file to parse
        :param data: The line in the file being parsed
        :return: The Gadget in that file
        """

        match fname: # Simply return filename from which Gadget was obtained; trust data is from filename
            case Filenames.asecl(): return Gadget.ENFORCER
            case Filenames.pcl2019(): return Gadget.CROSSOVER
            case Filenames.stoplights(): return Gadget.STOPLIGHT
            case Filenames.rlcl(): return Gadget.CAMERA

