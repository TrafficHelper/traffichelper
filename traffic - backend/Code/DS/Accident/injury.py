from enum import Enum
from Code.Interfaces.parser import Parser


class Injury(Parser, Enum):
    """
   All Injury levels considered in traffic application
   Limited by data
   Currently obtained from:
   - TrafficCollisionData.csv
   """

    # The four gradings of injuries
    UNINJURED = 0
    MINIMAL = 1
    MINOR = 2
    MAJOR = 3
    FATAL = 4

    def parse(self, filename, data):
        """
       Returns a list of Injuries given the data line
       :param filename: The file to read from (Currently TrafficCollisionData.csv)
       :param data: The line to extract from
       :return: bool, {Injury:int}: A key designating the levels of injury and, if they are all zero, a boolean designating whether any P.D. occurred. Vehicle injury will then also be added
       """

        # TrafficCollisionData.csv
        # Classification_Of_Accident (09)
        # Num_of_Injuries (20)
        # Num_of_Minimal_Injuries (21)
        # Num_of_Minor_Injuries (22)
        # Num_of_Major_Injuries (23)
        # Num_of_Fatal_Injuries (24)

        # The second element should be the sum of the next four elements and another category
        # If the above four are zero it is UNINJURED by default

        minim = Parser.clean(data[21])
        minor = Parser.clean(data[22])
        major = Parser.clean(data[23])
        fatal = Parser.clean(data[24])
        other = Parser.clean(data[20]) - (minim + minor + major + fatal)  # Other levels of injury is total injuries minus any graded injury
        # We will assume that other injuries are UNINJURED by default; this may not be true but no more specific information can be obtained

        # In the case of only property damage occurring, this should be given to the Outcome parser which will add on the vehicle injuries as well
        return False if data[9] == '03 - P.D. only' else True, {Injury.FATAL: fatal, Injury.MAJOR: major, Injury.MINOR: minor, Injury.MINIMAL: minim, Injury.UNINJURED: other}  # If True is returned then the dict should be zero
