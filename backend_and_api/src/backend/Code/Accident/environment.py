from __future__ import annotations

from enum import Enum

from backend.Code.Interfaces.parser import Parser

class Environment(Enum):

    """
    Enum representing the list of potential environments traffic experiences
    Combination of:
    - Surface: Road_Surface_Condition
    - Weather: Environment_Condition
    - Visibility: Light
    """

    IDEAL = 0
    NORMAL = 1
    ABNORMAL = 2
    DEVIANT = 3
    TROUBLESOME = 4
    EXTREME = 5

    @staticmethod
    def forname(v:str):
        match v:
            case "IDEAL": return Environment.IDEAL
            case "NORMAL": return Environment.NORMAL
            case "ABNORMAL": return Environment.ABNORMAL
            case "DEVIANT": return Environment.DEVIANT
            case "TROUBLESOME": return Environment.TROUBLESOME
            case "EXTREME": return Environment.EXTREME

    @staticmethod
    def score(surf: Surface, climate: Weather, luminosity: Visibility):
        """
        Returns a grading in terms of environment quality based on the
        Road Surface, Road Weather, Road Visibility
        :param surf: Surface parameter
        :param climate: Weather parameter
        :param luminosity: Visibility parameter
        :return:
        """
        # TODO Create better weighting for environment
        sval = 10 if surf.value == 99 else surf.value
        cval = 8 if climate.value == 99 else climate.value
        gval = 9 if luminosity.value == 99 else luminosity.value
        return int((sval + cval + gval) / 27.0 * 5)  # Crude approximation

    @staticmethod
    def grading(score:int):
        match score:
            case 0:
                return Environment.IDEAL
            case 1:
                return Environment.NORMAL
            case 2:
                return Environment.ABNORMAL
            case 3:
                return Environment.DEVIANT
            case 4:
                return Environment.TROUBLESOME
            case 5:
                return Environment.EXTREME
            case _:
                raise ValueError("Impossible grading score!")

    @staticmethod
    def extract(instruction, line):
        """
        For each of the Surface, Weather, Visibility, classes:
        Extract the number of the position and return whether the correct value matches it.
        :param instruction: Type representing Surface, Weather or Visibility
        :param line: The line to extract from
        :return: The requisite weather type
        """
        # Value is of form num-designation
        # Variable Road_Surface_Condition in TrafficCollisionData.csv (11)
        # Variable Environment_Condition in TrafficCollisionData.csv (12)
        # Variable Light in TrafficCollisionData.csv (13)
        specified = {Surface: 11, Weather: 12, Visibility: 13}
        parts = [comp.strip() for comp in line[specified[instruction]].split('-')]  # Index in form 'code - designation'
        # Following should work given advanced variable property inference
        if len(parts) != 2:
            return instruction.UNKNOWN  # Cannot parse instruction
        if parts[0][0] == '"':
            parts[0] = parts[0][1:]
        if parts[0][-1] == '"':
            parts[0] = parts[0][-1:]

        index, name = int(parts[0]), parts[1]
        for elem in instruction:
            if elem.value == index:
                return elem
        return instruction.UNKNOWN


class Surface(Parser, Enum):
    """
    Enum representing all Surface types considered in application
    Constrained by data
    """

    UNKNOWN = 0
    DRY = 1
    WET = 2
    SNOW = 3
    SLUSH = 4
    HARD = 5
    ICE = 6
    MUD = 7
    UNSTABLE = 8
    SPILLED = 9

    OTHER = 99 # 99

    def parse(self, filename, line):
        return Environment.extract(Surface, line)


class Visibility(Parser, Enum):
    """
    Enum representing all Visibility types considered in traffic application
    Constrained by data
    """

    UNKNOWN = 0
    DAY = 1
    DAWN = 3
    DUSK = 5
    DARK = 7

    OTHER = 99 # 99

    def parse(self, filename, line):
        return Environment.extract(Visibility, line)


class Weather(Parser, Enum):
    """
    Enum representing all Weather types considered in application
    Constrained by data
    """

    UNKNOWN = 0
    CLEAR = 1
    RAIN = 2
    SNOW = 3
    SLEET = 4
    SQUALL = 5
    WIND = 6
    HAZE = 7

    OTHER = 99 # 99

    def parse(self, filename, line):
        return Environment.extract(Weather, line)
