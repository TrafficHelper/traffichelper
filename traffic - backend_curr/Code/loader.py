import csv
import random

from Code.DS.Accident.accident import Accident
from Code.DS.Atomic.gadget import Gadget
from Code.DS.Atomic.vehicle import Vehicle
from Code.DS.Structural.graph import Graph, Edge, Node
from Code.DS.Structural.section import Section
from Code.DS.Temporal.recurrence import Recurrence
from Code.DS.Temporal.time import Time
from Code.DS.environment import Environment
from Code.Interfaces.cost import Cost
from Code.Utils.adminutils import AdminUtils
from Code.Utils.preferences import Preferences
from Code.filenames import Filenames


class Loader:

    @staticmethod
    def load():
        """
        Uses all data contained in the /Data to construct a Graph representing the traffic network
        From this, further operations may be conducted.
        :return: Graph representing all parsed Data
        """

        # Step 1: Load network structure
        network = Graph()
        network.parse(Filenames.centrelines(), []) # Redundant params.

        # Step 1.5: Create EdgeID - Edge mapping scheme and Node list
        edges = network.spread()
        mapping:{str:Edge} = {edg.segID:edg for edg in edges} # Should not face any replacement, as each segID is unique
        points:[Node] = network.nodes

        # Step 2: Load Accident Data
        acf = Filenames.collisiondata()
        quota = sum(1 for _ in open(Filenames.rlcl())) - 1 # Number of CAMERAS there exist (should add)
        with open(acf) as accidents:
            rdr = csv.reader(accidents)
            first = True # Want to skip first line of designations, already know that
            for line in rdr:
                if not first:
                    instance = Accident()
                    instance.parse(acf, line)
                    # Collision file tells us whether an accident occurred at an Edge or Node/Intersection
                    # This is the best on the data we can know (Geo ID is insufficient), and thus we must choose a random position from the classification
                    rand_segment:Section = random.choice(points) if line[8] == 'Intersection' else random.choice(list(mapping.values()))
                    rand_segment.stats.accidents.append(instance)
                    if line[14] == 'Traffic Signal':
                        rand_segment.modify(Gadget.STOPLIGHT, True, True) # Add STOPLIGHT Gadget if the reason was a traffic light, the only way we can ever know
                        if quota > 0:
                            rand_segment.modify(Gadget.CAMERA, True, True) # Add CAMERA Gadget if there is quota remaining
                            quota-=1 # If the quota remains, it's fine, as it was impossible to determine their location anyway
                    # Add accident to list of accidents on that edge's stats
                    # Probabilistically, each Section should not be devoid of Accident, especially as the network has been slimmed due to time-cost
                first = False

        # Step 3a: Load Mid-block Traffic Volumes
        mvd:[str] = Filenames.midblockvols()
        for filename in mvd:
            with open(filename) as mid_block_volume:
                rdr = csv.reader(mid_block_volume)
                first = True
                for line in rdr:
                    if not first: # Assign random intersections to the Edges as Geo ID are insufficient
                        instance = Vehicle.RATIOS.parse(filename, line)
                        random_edge:Section = random.choice(list(mapping.values()))
                        for veh in instance:
                            random_edge.stats.flows[veh] = Recurrence(Time.RECURRENCE, instance[veh])
                    first = False

        # Step 3b: Load Intersection Traffic Volumes
        ivd:[str] = Filenames.intersectvols()
        for filename in ivd:
            with open(filename) as intersection_volume:
                rdr = csv.reader(intersection_volume)
                first = True
                for line in rdr:
                    if not first: # Again, assign random intersections to the volumes as the Geo ID data is insufficient to ascertain exact location
                        instance = Vehicle.RATIOS.parse(filename, line) # Breakdown of Vehicle by volume
                        random_node:Section = random.choice(points)
                        for veh in instance:
                            random_node.stats.flows[veh] = Recurrence(Time.RECURRENCE, instance[veh])
                    first = False

        # Step 4: Load all Traffic Gadget

        # 4a: ENFORCER
        ase = Filenames.asecl()
        with open(ase) as enforcers:
            rdr = csv.reader(enforcers)
            first = True
            for line in rdr:
                if not first:
                    enforcer = Gadget.ENFORCER.parse(ase, line)
                    random_edge = random.choice(list(mapping.values()))
                    random_edge.modify(enforcer, True, True) # Just add an enforcer for now ..., changing occurs in user-given permission
                first = False

        # 4b: CROSSOVER
        crs = Filenames.pcl2019()
        with open(crs) as crossovers:
            rdr = csv.reader(crossovers)
            first = True
            for line in rdr:
                if not first:
                    crossover = Gadget.CROSSOVER.parse(crs, line)
                    random_edge = random.choice(list(mapping.values()))
                    random_edge.modify(crossover, True, True) # Just add a crossover for now ..., change it later
                first = False

        # 4c: STOPLIGHT
        # Stoplights are contained in the accident's data, so this is loaded in the accident loader section

        # 4d: CAMERA
        # Red Light Camera Locations can ONLY be at a STOPLIGHT location which is determined in Part 2, thus so is this.

        return network

    @staticmethod
    def setup():
        """

        Sets up things for initializing the application
        Loads the Traffic Network,
        :return:
        """

        network = Loader.load() # The fully initialized and ready application
        preferences = Preferences(Vehicle.CAR, Environment.OPPOSED, Accident.STANDARD(), Cost.STANDARD()) # The Cost is a function
        user = AdminUtils(network)

        # Demonstration




