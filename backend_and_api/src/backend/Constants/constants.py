import copy
import csv
import pickle # Used when storing accidents list

from backend.Code.Atomic.gadget import Gadget
from backend.Code.Atomic.vehicle import Vehicle
from backend.Code.Accident.accident import Accident
from backend.Constants.filenames import Filenames

LOCATIONS = ['Ottawa, Canada', 'Gatineau, Canada'] # Network domain
FEATURES = ['drive'] # We will include drive features only to preserve efficiency

CLI_INFO_FILEPATH = 'C:/Projects/xoutput/Documentation/cli-instructions' # Filepath of cli information, called with 'man'

DEFAULT_VEHICLE_BREAKDOWN = Vehicle.OTHER.list_vehicles(100) # Default breakdown of vehicles by type on road segment
CHANCE_FACTOR = 1e-10 # Chance of an accident happening on a road when none has happened before
DEFAULT_SPEED_LIMIT = 50 # Ontario's speed limit

# Prices in bulk
EDGE_ADD_COST = 15 # Price to add road per meter
EDGE_REMOVE_COST = 5 # Price to remove road per meter


# By default, we have a single-lane road with speed limit of 50km/h for Ottawa, no stoplights and no speed enforcers (cameras)
DEFAULT_GADGETS_IMPLEMENTATION = {Gadget.LANE:1, Gadget.SPEED_INCREASE:DEFAULT_SPEED_LIMIT//Gadget.DISCRETION.value, Gadget.STOP_LIGHT:0, Gadget.SPEED_ENFORCER:0}

TRAFFIC_NETWORK_FILEPATH = 'C:/Projects/xoutput/src/backend/Data/network.graphml'  # Filepath of cached raw GraphML-type traffic network
TRAFFIC_NETWORK_BACKUP_FILEPATH = 'C:/Projects/xoutput/src/backend/Data/network_backup.graphml'

ACCIDENTS_DEFAULT = [] # Default set of accidents

PEDESTRIAN_MAX_SPEED = 5.5 # Maximum speed in kph of pedestrian
BICYCLE_MAX_SPEED = 20 # Maximum speed in kph of bicycle

def firstacc():
    afn = Filenames.collisiondata()
    rdr = csv.reader(open(afn))
    next(rdr)
    results = []
    for line in rdr:
        acc = Accident()
        acc.parse(afn, line)
        results += [acc]
        break
    return results

ACCIDENTS_DEFAULT = firstacc()

NORMAL_BUDGET = 10**6 # Normal budget for gadgets

# Initial template which is added to all nodes and edges by default. 'cost' and 'risk' are computed from the other parameters if to be changed
INIT_TEMPLATE = {'cost':0, 'risk':CHANCE_FACTOR, 'accidents':copy.copy(ACCIDENTS_DEFAULT), 'flows':DEFAULT_VEHICLE_BREAKDOWN, 'gadgets': DEFAULT_GADGETS_IMPLEMENTATION}

INTERSECTION_TRAVERSAL_TIME = 2 # Average time taken to cross intersection. Artificially added for increased accuracy as networkx doesn't support it
INTERSECTION_LENGTH = 2 # Length of intersection in meters, incorporating this will give more accurate values

def domain(filename:str):
    elements = frozenset()
    rdr = csv.reader(open(filename))
    next(rdr) # Skip unneeded first line
    for line in rdr:
        acc = Accident()
        acc.parse(filename, line)
        elements = elements.union(frozenset([acc]))
    return elements

DOMAIN_ACCIDENTS_FILENAME = 'C:/Projects/xoutput/src/backend/Data/accidents_objects.pickle'

# # Following is commented and called only once:
# with open(DOMAIN_ACCIDENTS_FILENAME, 'wb') as daf:
#     pickle.dump(domain(Filenames.collisiondata()), daf)
# DOMAIN_ACCIDENTS = pickle.load(open(DOMAIN_ACCIDENTS_FILENAME, 'rb')) # List of all accidents which user should consider


