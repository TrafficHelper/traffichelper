from __future__ import annotations

import datetime
import math

from Interfaces.parser import Parser
from filenames import Filenames


class Time(Parser):

    """
    Represents the fundamental unit of time considered in the application
    Time is measured in minutes
    Time consists of a repeating period length (ex. Weekday, Season) equipped with a potential "absolute" time; this allows inter-comparison between times of different periods
    The sum or difference of two absolute times is also absolute, otherwise it is relative by default, where absolute is None
    Each time is a float (modulo) the cyclic time
    """

    RECURRENCE = 60 * 24 * 7  # Number of minutes in week, fundamental time repetition

    def __init__(self, period: int = RECURRENCE):
        if period <= 0:
            raise ValueError('Period must be positive')
        self.period = period

        self.time = 0  # Relative time (modulo the period) stored
        self.absolute = None  # Represents the "absolute" time for some definition of "absolute"; Often signifying minutes since the *NIX epoch, though can be otherwise. Can be negative

    def set(self, time: int, absolute: bool = False):
        """
       Sets to the given time, and if absolute, treats it as such
       :param time: The time to set to
       :param absolute: Whether this is the absolute time or not
       :return:
       """
        self.absolute = time if absolute else None
        self.time = time % self.period

    def based(self):
        """
       Return whether the current time supports absolute values
       :return: Whether the current time object contains an absolute value
       """
        return self.absolute is not None

    def compatible(self, other: Time):
        """
       Returns whether two times are compatible, i.e. have the same period
       :param other: The other time
       :return: Whether the two times are equivalent
       """
        return self.period == other.period

    def relativize(self, period: int = RECURRENCE):
        """
       Return a Time with the new period and same "relative" time
       Can only work if the object already possesses some absolute value
       :param period: The new period to set the time object to
       :return: The new period of the time
       """
        if not self.based():
            raise ValueError("Cannot rebase non-absolute Time")
        new = Time(period)
        new.set(self.absolute, True)
        return new

    def __add__(self, other: Time):
        return self.addsub(other, True)

    def __sub__(self, other: Time):
        return self.addsub(other, False)

    def addsub(self, other: Time, add: bool):
        """
       Adds or subtracts the two times from each other
       :param other: The other time
       :param add: bool designating 'add' if True, 'subtract' if False
       :return: The sum or difference of the two times
       """
        op = 1 if add else -1
        if self.based() and other.based():  # Both times are absolute, can set to whatever base we desire, choose lcm of bases by default
            result = Time(math.lcm(self.period, other.period))
            result.set(self.absolute + op * other.absolute, True)
            return result
        # At least one time is relative here
        if self.compatible(other):
            result = Time(self.period)
            result.set(self.time + op * other.time, False)  # Sadly we cannot propagate the absolute times
            return result
        raise ValueError("Cannot add non-absolute times with unequal periods")  # We cannot add relative times with different bases

    def __eq__(self, other: Time):
        """
       Returns whether two times are the same
       Two times are (functionally) identical when their relative times are the same modulo equal periods
       :param other: Time; the other time to compare to
       :return: Whether two times are equal to each other
        """
        return self.compatible(other) and self.time == other.time

    def equivalent(self, other:Time):
        """
        Convenience methods to determine whether two Time represent the same absolute value
        They represent the same absolute value if both support absoluteness (based) and their absolute values are the same
        The periods are not necessarily equal.
        :param other: Time to compare with
        :return: Whether the two times are equivalent
        """
        return self.based() and other.based() and self.absolute == other.absolute

    def __str__(self):  # String representation for easy conversion to user-readable format
        if self.based():
            return str(self.absolute) + ' min from epoch init.'
        return str(self.time) + ' min from cycle of length ' + str(self.period) + ' init.'

    def parse(self, filename, data):

        """
        Parse a Time object from the file-dependent data:
        The files are currently:
         - TrafficCollisionData.csv
         - RoadCentrelines.csv
         - MidblockVolume[2022, 2023].csv
         - IntersectVolume[2015, 2023].csv
        This is an interpreter in plurality; it may return more than a single Time result for each row.
        Thus, it is not a mutator for the referent Time argument; it is suggested that be a dummy.
        :param filename: The name of the file being parsed from
        :param data: The respective line in the parsed file
        :return: The file-dependent Time object from the data
        """

        mos = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        if filename in Filenames.intersectvols().values(): # IntersectVolume20[15, 23].csv
            year, month, day = data[5].split('-')  # Date (5) : yyyy-mmm-dd
            return Time.create(datetime.datetime(int(year), mos[month], int(day)))

        if filename in Filenames.midblockvols().values():  # MidblockVolume20[22, 23].csv
            return Time.create(datetime.datetime(int(data[2]), 1, 1)) # Year (2) : yyyy

        if filename in Filenames.centrelines():
            # RoadCentrelines.csv
            # GEOMETRY_CREATED_DATE (8)
            # GEOMETRY_MODIFIED_DATE (9)
            # STATUS_CREATED_DATE (11)
            # STATUS_MODIFIED_DATE (12)
            # ADD_CREATED_DATE (36)
            # ADD_MODIFIED_DATE (37)
            result = []
            for index in [7, 8, 10, 14, 36]:
                temporal = data[index]  # yyyy/mm/dd hh:mm:ss+hh format
                if temporal == '': # If time field empty, add random time of 1:01AM on 1st January 2020
                    result.append(Time.create(datetime.datetime(2020, 1, 1, 1, 1)))
                else:
                    date, time = temporal.split(' ')
                    year, month, day = date.split('/')
                    hour, minutes, seconds = time.split(':')
                    result.append(Time.create(datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))))
            return result

        if filename in Filenames.collisiondata():
            # TrafficCollisionData.csv
            year, month, day = data[5].split('/') # Accident_Date (5)
            hour = 0
            minute = 0
            if data[6] != 'Unknown':
                hour, minute = data[6].split(':')  # Accident_Time (6)
            return Time.create(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)))

        raise ValueError(' Cannot parse time from data ')

    @staticmethod
    def create(dt: datetime.datetime):
        absolute = int(dt.timestamp())//60  # Minutes since epoch
        result = Time()
        result.set(absolute, True)
        return result
