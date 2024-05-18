from __future__ import annotations

import datetime

from Code.Accident.outcome import Outcome
from Code.Accident.environment import Environment, Surface, Visibility, Weather

from Code.Interfaces.parser import Parser
from Code.filenames import Filenames


class Accident(Parser): # TODO Re-include Section and associated methods after fixing it
    """
    Class representing each individual accident,
    - location: Location in Network Component (Edge: Road OR Node: Intersection)
    - time: Time interval of accident occurring
    - weather: Weather Type
    - outcome: The list of accident levels experienced by each vehicle type
    """

    def __init__(self, start: datetime.datetime = datetime.datetime.now(), end: datetime.datetime = datetime.datetime.now(), environment: Environment = None, outcome: Outcome = None):
        # self.location = location
        # Start and end times are the same when loading accidents from the data
        self.start = start
        self.end = end
        self.environment = environment
        self.outcome = outcome

    def parse(self, filename, data):
        fn = Filenames.collisiondata()
        env = Environment.grading(Environment.score(Surface.UNKNOWN.parse(fn, data), Weather.UNKNOWN.parse(fn, data), Visibility.UNKNOWN.parse(fn, data)))  # Get environment as combination of surface, weather and visibility
        out = Outcome()
        out.parse(filename, data)  # Get result of parsing data from filename
        occ = datetime.datetime.now()  # Get time of occurrence as parsed from collision data and time
        # self.location = None
        self.start = occ
        self.end = occ
        self.environment = env
        self.outcome = out

    @staticmethod
    def standard():
        """
        Returns the list of standard unacceptable accidents which are considered by the application
        The accidents have a default time and are under the equivalence method, i.e. two accidents are equivalent iff they have the same outcome and environment
        Here, the standard unacceptable accidents is the domain of the accident file
        :return: The List of standard considered accidents
        """
        return {*()}

        # first = True
        # elements = {*()}
        # coll = Filenames.collisiondata()
        # for line in csv.reader(open(coll)):
        #     if first:
        #         first = False
        #         continue
        #     acc = Accident()
        #     acc.parse(coll, line)
        #     elements.add(acc)
        # return elements

