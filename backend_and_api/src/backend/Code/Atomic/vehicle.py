from enum import Enum

from backend.Code.Interfaces.parser import Parser
from backend.Constants.filenames import Filenames


class Vehicle(Parser, Enum):
    """
    Enum of all considered vehicle types in traffic application
    Pedestrians and Bicycles are also considered a Vehicle, though the difference of motor vehicle networks and pedestrian paths may contribute to a shortcoming in accurately assesing them
    The set of all such types is limited due to the data
    """

    # Avg. ratio of CAR:TRUCK:MOTORCYCLE in Urban Road
    # Obtained from https://publications.gc.ca/collections/Collection/Statcan/11-621-M/11-621-MIE2005028.pdf and https://www.advrider.com/f/threads/ratio-of-motorcycles-to-cars-trucks.19083/
    RATIOS = (432, 16, 27)

    PEDESTRIAN = 1
    BICYCLE = 2
    MOTORCYCLE = 3
    CAR = 4
    TRUCK = 5  # Found in IntersectVolume20[15, 22].csv
    OTHER = 6

    def parse(self, filepath, data):

        """
       Parses the list of number of all vehicle types contained in the data
       Parses from three filepaths; Collision Data, Intersection Volumes and Mid-block Volumes
       :param filepath: The file from which data is being parsed from
       :param data: The row from the file to parse
       :return: The Number of vehicles of each type listed in data
        """

        # Here line is a tuple

        pedestrians = 0
        bicycles = 0
        motorcycles = 0
        cars = 0
        trucks = 0
        others = 0

        # All given file names should be one of these three cases
        if filepath == Filenames.collisiondata():

            # TrafficCollisionData.csv
            # Num_Of_Vehicle (15)
            # Num_Of_Pedestrians (16)
            # Num_Of_Bicycles (17)
            # Num_Of_Motorcycles (18)

            cars = Parser.clean(data[15])
            pedestrians = Parser.clean(data[16])
            bicycles = Parser.clean(data[17])
            motorcycles = Parser.clean(data[18])

        elif filepath in Filenames.intersectvols().values():
            # IntersectVolume20[15, 23].csv
            # All_Motorized_Vehicles_AADT_24_ (1)
            # Truck_Percent (2)
            # Pedestrians_Not_Factored (3)
            # Bicycles_Not_Factored (4)
            designations = {'2015':5, '2016':3, '2017':3, '2018':3, '2019':1, '2021':2, '2022':1, '2023':1}
            i = 0
            for e in designations:
                if e in filepath:
                    i = designations[e]
            # i = 5 if '2015' in filepath else 3 if '2016' in filepath else 3 if '2017' in filepath else 3 if '2018' in filepath else 1 if '2019' in filepath else 2 if '2021' in filepath else 1 if '2022' in filepath else 1 if '2023' else 0
            motor, trucks, pedestrians, bicycles = (data[i], data[i+1], data[i+1], data[i+3])
            cars = Parser.clean(motor)  # Currently denotes number of motor vehicles
            trucks = int(Parser.clean(trucks) * cars)  # Percentage of trucks in motor vehicles scaled to number of motor vehicles
            cars -= trucks  # Ostensibly designates number of cars after removing trucks; we make a simplifying (though incorrect) assumption that there are either cars or trucks
            pedestrians = Parser.clean(pedestrians)
            bicycles = Parser.clean(bicycles)

        elif filepath in Filenames.midblockvols().values():

            # MidblockVolume20[22, 23].csv
            # All_Motorized_Vehicles_AADT_24_ (3)

            vehicles = Parser.clean(data[3])
            cars, trucks, motorcycles = Vehicle.distribute(Vehicle.RATIOS.value, vehicles)  # Distribute the vehicles according to the standard ratio

        return {Vehicle.PEDESTRIAN: pedestrians, Vehicle.BICYCLE: bicycles, Vehicle.MOTORCYCLE: motorcycles, Vehicle.CAR: cars, Vehicle.TRUCK: trucks, Vehicle.OTHER: others}

    @staticmethod
    def distribute(distribution: (), quantity: int, approximate: bool = True):
        """

       Convenience method to create a distribution of the given quantity in the given proportions
       - A non-approximate distribution is a simple ratio calculation
       - An approximate distribution distributes the remaining numbers after integer division to the "closest" other terms

       :param distribution: The distribution policy
       :param quantity: The number to distribute
       :param approximate: Whether to have the final result in float or integer
       :return: The quantity distributed among the distribution
       """

        if not approximate:
            n = sum(distribution)
            return (val / n * quantity for val in distribution)  # The final distribution

        dist = Vehicle.distribute(distribution, quantity, False)
        decomposition = [(int(elem), elem - int(elem)) for elem in dist]  # The integer and decimal parts of the distribution
        floored = (elem[0] for elem in decomposition)  # Floor values
        remaining = quantity - sum(floored)  # We have to distribute the remaining quantity somewhere ...
        optimal = [e for e in sorted([elem[1] for elem in decomposition])][:-remaining]  # Return k largest fractional parts
        decomposition = [(e[0] + (1 if e[1] in optimal else 0), e[1]) for e in decomposition]  # Increment for decimal parts along k closest positions
        return [e[0] for e in decomposition]  # Return new decomposition after it has been modified

    @staticmethod
    def list_vehicles(avg):
        amounts = Vehicle.distribute(Vehicle.RATIOS.value, avg)
        return {Vehicle.PEDESTRIAN: 10, Vehicle.BICYCLE:5, Vehicle.MOTORCYCLE: amounts[2], Vehicle.CAR: amounts[0], Vehicle.TRUCK: amounts[1], Vehicle.OTHER: 5}

    # A function which returns the vehicle object for the OSMnx serialized str data
    @staticmethod
    def for_name(veh_name:str):
        """
        :param veh_name: The OSMnx serialized str data
        :return: Convenience function to return Vehicle obj for OSMnx serialized str data
        """
        return {'Vehicle.PEDESTRIAN': Vehicle.PEDESTRIAN, 'Vehicle.BICYCLE': Vehicle.BICYCLE, 'Vehicle.MOTORCYCLE': Vehicle.MOTORCYCLE, 'Vehicle.CAR': Vehicle.CAR, 'Vehicle.TRUCK': Vehicle.TRUCK, 'Vehicle.OTHER': Vehicle.OTHER}[veh_name]





