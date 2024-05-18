import itertools


class Filenames:

    """
    List of Filenames used throughout the application\n
    Each filename consists of a string\n
    Currently, they include:
        - List of Traffic Accidents (TrafficCollisionData.csv)
        - Road network (RoadCentrelines.csv)
        - Road segment volumes (MidblockVolume20[22, 23].csv)
        - Road Intersection volumes (IntersectVolume20[15, 23].csv)

        - Automated Speed Enforcement Cameras (AutomatedSpeedEnforcementCameraLocations.csv)
        - Pedestrian Crossover Locations (PedestrianCrossoverLocations2019.csv)
        - Red Light Camera Locations (RedLightCameraLocations.csv)
    \nEach file type may be accessed by a static method which returns the filename, or an association of year to respective file
    \nIn the latter case, calling that year will return the designated file name
    """

    # Gadgets

    @staticmethod
    def asecl():
        """
        :return: The filename for Automated Speed Enforcement Cameras locations
        """
        return 'C:/Projects/trafficWise/Data/Gadgets/AutomatedSpeedEnforcementCameraLocations.csv'

    @staticmethod
    def pcl2019():
        """
        :return: The Pedestrian Crossover Locations
        """
        return 'C:/Projects/trafficWise/Data/Gadgets/PedestrianCrossoverLocations2019.csv'

    @staticmethod
    def stoplights():
        """
        :return: The file containing the list of all Stoplight Gadget locations
        """
        # TODO Method Stub
    @staticmethod
    def rlcl():
        """
        :return: Red Light Camera Locations
        """
        return 'C:/Projects/trafficWise/Data/Gadgets/RedLightCameraLocations.csv'

    # Other

    @staticmethod
    def collisiondata():
        """
        :return: The filename for Traffic Collision Data
        """
        return 'C:/Projects/trafficWise/Data/TrafficCollisionData.csv'

    @staticmethod
    def centrelines():
        """
        :return: The filename for road centrelines
        """
        return 'C:/Projects/trafficWise/Data/RoadCentrelines.csv'

    MIDBLOCK_DOMAIN = range(2022, 2023 + 1) # List of all years considered for midblock, road segment traffic volumes

    @staticmethod
    def midblockvols():
        """
        :return: A dictionary containing the year and segment volume filename associated with it
        """
        return {year:'C:/Projects/trafficWise/Data/Volumes/MidblockVolume'+str(year)+'.csv' for year in Filenames.MIDBLOCK_DOMAIN}

    INTERSECTION_DOMAIN = list(range(2015, 2020)) + list(range(2021, 2023 + 1)) # List of all years considered for road intersection volumes excluding 2020

    @staticmethod
    def intersectvols():
        """
        :return: A dictionary containing the year and the intersection volume filename associated with it
        """
        return {year:'C:/Projects/trafficWise/Data/Volumes/IntersectVolume'+str(year)+'.csv' for year in Filenames.INTERSECTION_DOMAIN}
