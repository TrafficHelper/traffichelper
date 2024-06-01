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

        return 'C:/Projects/xoutput/src/backend/Data/Gadgets/AutomatedSpeedEnforcementCameraLocations.csv' # 23

    @staticmethod
    def pcl2019():
        """
        :return: The Pedestrian Crossover Locations
        """
        return 'C:/Projects/xoutput/src/backend/Data/Gadgets/PedestrianCrossoverLocations2019.csv'

    # @staticmethod
    # def stoplights():
    #     """
    #     :return: The file containing the list of all Stoplight Gadget locations
    #     """
    #

    @staticmethod
    def rlcl():
        """
        :return: Red Light Camera Locations
        """
        return '../Data/Gadgets/RedLightCameraLocations.csv' # [22]

    # Other

    @staticmethod
    def collisiondata():
        """
        :return: The filename for Traffic Collision Data
        """
        return 'C:/Projects/xoutput/src/backend/Data/TrafficCollisionData.csv' # [25]

    # @staticmethod
    # def centrelines():
    #     """
    #     :return: The filename for road centrelines
    #     """
    #     return '../Data/RoadCentrelines.csv' # [24]

    MIDBLOCK_DOMAIN = range(2022, 2023 + 1) # List of all years considered for midblock, road segment traffic volumes

    # Volumes

    @staticmethod
    def midblockvols():
        """
        :return: A dictionary containing the year and segment volume filename associated with it
        """
        # [34, 35]
        # prefix = '../Data/Volumes/MidblockVolume'
        prefix = 'C:/Projects/xoutput/src/backend/Data/Volumes/MidblockVolume'
        return {year:prefix+str(year)+'.csv' for year in Filenames.MIDBLOCK_DOMAIN}

    INTERSECTION_DOMAIN = list(range(2015, 2020)) + list(range(2021, 2023 + 1)) # List of all years considered for road intersection volumes excluding 2020

    @staticmethod
    def intersectvols():
        """
        :return: A dictionary containing the year and the intersection volume filename associated with it
        """
        # [26, 27, 28, 29, 30, 31, 32, 33]
        # prefix = '../Data/Volumes/IntersectVolume'
        prefix = 'C:/Projects/xoutput/src/backend/Data/Volumes/IntersectVolume'
        return {year:prefix+str(year)+'.csv' for year in Filenames.INTERSECTION_DOMAIN}
