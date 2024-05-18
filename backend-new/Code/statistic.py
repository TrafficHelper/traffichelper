from __future__ import annotations

import math

from Code.DS.Accident.accident import Accident
from Code.DS.Atomic.vehicle import Vehicle
from Code.DS.Temporal.recurrence import Recurrence
from Code.DS.Temporal.time import Time
from Code.Interfaces.parser import Parser
from Code.filenames import Filenames


class Statistic:

    """
    Represents a large majority of statistical data associated with a section
    Currently akin to a "Data Packet" of information
    Consists of a:
    - list of Acctmp : Density of accidents at each given time
    - Vehicle to Recurrence flows : The frequency (in absolute number) of the vehicles on that (segment) over the measured (cyclical) time
    - ==> Vehicle to Recurrence times : The amount of time (in minutes) it takes for a Vehicle to cross the segment of that statistic, at a given starting time
    The Recurrence period is intended to be the standard "Time.RECURRENCE" cyclical period
    """

    def __init__(self, accidents: [Accident] = None, flows:{Vehicle:Recurrence} = None, times:{Vehicle:Recurrence} = None):
        self.accidents = accidents
        self.flows = flows
        self.times = times

    def __eq__(self, other: Statistic):
        """
        Returns whether the two types are equal to each other
        Two Statistic are equal if they have the same accident values, flow values and time values
        :param other: The other Statistic to compare to
        :return: Whether the two Statistic are equal to each other
        """
        return self.accidents == other.accidents and self.flows == other.flows and self.times == other.times

    def extract(self, accidents:[[]], midflow:[], inflow:[], myear:int = 2023, inyear:int = 2023, length:int = 30):
        """
        Extracts all statistical data from the given file
        The input will consist of a list of lists of data; each one designates the statistics ostensibly related to only one Section
        Consequently, no verification checks are conducted (this may be subject to change)
        :param accidents: The list of all accidents to parse
        :param midflow: The list of all flows pertaining to that segment from mid-block volumes
        :param inflow: The list of all flows pertaining to that segment from intersection volumes
        :param myear: The year for which midblock data was collected
        :param inyear: The year for which intersection data was collected
        :param length: The length of the ostensible segment this pertains to
        :return: The parsed data
        """

        # Step 1: Record all accidents
        troubles = []
        fn = Filenames.collisiondata()
        for row in accidents:
            acc = Accident()
            acc.parse(fn, row)
            troubles.append(acc)
        self.accidents = troubles # Parse accident data

        # Step 2: Record all traffic flows
        mid = [Vehicle.OTHER.parse(Filenames.midblockvols()[myear], i) for i in midflow]  # Parse vehicle densities based on mid-block flow
        ints = [Vehicle.OTHER.parse(Filenames.intersectvols()[inyear], i) for i in inflow] # Parse vehicle densities based on intersectional flow
        # Take vector average of all elements in final list

        final = {e:0.0 for e in Vehicle}
        del final[Vehicle.RATIOS]
        n = len(mid) + len(ints)
        for elem in mid:
            for th in final:
                final[th]+=elem[th]
        for elem in ints:
            for th in final:
                final[th]+=elem[th]

        final = {e:Recurrence(Time.RECURRENCE, math.floor(final[e]/n)) for e in final} # Due to lack of data currently cannot create nuanced recurrence
        self.flows = final

        # Step 3: Compute expected times GIVEN KNOWLEDGE OF flows
        self.tempest(length)

    def tempest(self, length:float, limit:float = 0.833):

        """
        PRIVATE METHOD
        Given a PREVIOUSLY ASSIGNED series of traffic flows, compute the expected times for each vehicle
        :return: The expected times for each vehicle to traverse the length given top speed
        """

        standard = length/limit # Standard time in minutes given km/min (unconventional), assuming no impediment
        ts = {}
        # Compute aggregate impediment
        aggregate = Recurrence()
        for vehicle in self.flows:
            aggregate+=self.flows[vehicle]

        lower = aggregate.range()[0]
        # Such that the lowest possible time is the standard time; also add epsilon to account for zero as minimal range
        aggregate = aggregate.multiply(standard/(lower + 0.01)*0.001)
        # TODO Fix Zero division error

        for vehicle in self.flows:
            ts[vehicle] = aggregate # So far it is assumed the same for all vehicles;
        self.times = ts

    def __str__(self):
        return 'Statistic: '+str(self.accidents) + ', flows: ' + str(self.flows) + ', times: ' + str(self.times)

