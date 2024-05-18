"""
A suite of methods representing the interface between the frontend and backend
Either called in a REST API call or through similar means
These variables are specific to each individual run of the program (each unique account)
"""

import calendar
import datetime

import osmnx

import persistence
from Code.Atomic.gadget import Gadget
from Code.Atomic.vehicle import Vehicle
from Code.Accident.environment import Environment
from Code.Utils import utils
from Code.Utils.preferences import Preferences
from Code.Utils.utils import Utils
from Code.mutation import Mutation
from Code.user import User

# USER CREATION PAGE, MUST BE DONE
USER:User = User()
def create_user(admin:str):
    global USER
    USER = User(is_admin=True if admin == 'true' else False)

# PREFERENCE PAGE

# Selection

SELECTED_VEHICLE_DEFAULT:Vehicle = Vehicle.OTHER
SELECTED_VEHICLE:Vehicle = SELECTED_VEHICLE_DEFAULT
def select_vehicle(veh:str):
    """
    Called in the user webpage dropdown selection of a vehicle str form

    Ascribes it to a vehicle object
    :param veh: The vehicle name inputted
    :return: Assigns the user's choice of vehicle
    """
    veh_type = Vehicle.OTHER
    match veh:
        case 'PEDESTRIAN': veh_type = Vehicle.PEDESTRIAN
        case 'BICYCLE': veh_type = Vehicle.BICYCLE
        case 'MOTORCYCLE': veh_type = Vehicle.MOTORCYCLE
        case 'CAR': veh_type = Vehicle.CAR
        case 'TRUCK': veh_type = Vehicle.TRUCK
        case 'OTHER': veh_type = Vehicle.OTHER
    return veh_type

SELECTED_ENVIRONMENT_DEFAULT:Environment = Environment.NORMAL
SELECTED_ENVIRONMENT = SELECTED_ENVIRONMENT_DEFAULT
def select_environment(env:str):
    """
    Called in the user page environment selection dropdown when that is clicked.

    Given the user's selection of an environment from the dropdown, it creates that approximate such environment
    :param env: The string representing the input environment
    :return: The user's selection of the environment
    """
    env_type = Environment.NORMAL
    match env:
        case 'IDEAL': env_type = Environment.IDEAL
        case 'NORMAL': env_type = Environment.NORMAL
        case 'ABNORMAL': env_type = Environment.ABNORMAL
        case 'DEVIANT': env_type = Environment.DEVIANT
        case 'TROUBLESOME': env_type = Environment.TROUBLESOME
        case 'EXTREME': env_type = Environment.EXTREME
    return env_type

PATH_METRIC_DEFAULT = (1/3, 1/3, 1/3)
PATH_METRIC = PATH_METRIC_DEFAULT
def path_metric(safety_emphasis:str, time_emphasis:str, distance_emphasis:str):
    """
    Called for the webpage emphasis sliders when:
    - [Submit] button is chosen --> Accepts the values of each of those indices
    - [Reset] button is chosen --> Accepts the standard values of (1/3, 1/3, 1/3) in str form

    Give string values representing the user's emphasis on the path qualities (this is from the three sliders)
    Assigns this to its new cost metric per path.
    All emphases are normalized between 0, 1 inclusive.
    By default, the path metric is still (1/3, 1/3, 1/3) though.
    :param safety_emphasis: The emphasis on safety, string
    :param time_emphasis: The emphasis on time, string
    :param distance_emphasis: The emphasis on distance, string
    :return: Sets this to the preferred metric
    """
    assert safety_emphasis.isnumeric() and time_emphasis.isnumeric() and distance_emphasis.isnumeric()
    return float(safety_emphasis), float(time_emphasis), float(distance_emphasis)

# Creation
def obtain_preferences():
    """
    Called when the user clicks the [Finalize] button in the webpage after selecting their preferences
    :return: Creates a preferences object based on the user's Finalized choice; All preceding preferences should be chosen prior
    """
    USER.preferences = Preferences(SELECTED_VEHICLE, SELECTED_ENVIRONMENT, PATH_METRIC)

# USER PAGE

# Selection

START_NODE_DEFAULT = None # WARNING: THIS IS NONE - THE COORDINATE RECORDER FUNCTION MUST ALWAYS BE CHOSEN
START_NODE = START_NODE_DEFAULT
def select_start(position:str | (float, float)):
    """
    Called from the user webpage of:
    - the current position of the [Start] (blue) pin on the EMBEDDED MAP, a coordinate tuple
    or, with over-precedence, when
    - the [Finalize] button is selected for the |Start| field , a str input
    :param position: The input position designating the user's start
    :return: Functionally stores the accepted start Node
    """
    global START_NODE
    lat, long = osmnx.geocode(position) if type(position) is str else position
    START_NODE = osmnx.nearest_nodes(persistence.TRAFFIC_NETWORK, lat, long)

END_NODE_DEFAULT = None # WARNING: THIS IS NONE - THE COORDINATE RECORDER FUNCTION MUST BE CHOSEN
END_NODE = END_NODE_DEFAULT
def select_end(position:str | (float, float)):
    """
    Called from the user webpage of:
    - the current position of the [End] (red) pin on the EMBEDDED MAP, a coordinate tuple
    or, with over-precedence, when
    - the [Finalize] button is selected for the |End| field , a str input
    :param position: The input position designating the user's end
    :return: Functionally stores the accepted end Node
    """
    global END_NODE
    lat, long = osmnx.geocode(position) if type(position) is str else position
    END_NODE = osmnx.nearest_nodes(persistence.TRAFFIC_NETWORK, lat, long)

NUM_PATHS_DEFAULT:int = 1
NUM_PATHS = NUM_PATHS_DEFAULT
def select_num_paths(num_paths:str):
    """
    Selects the number of paths from the dynamic tracker of the NUM_PATHS field in the website
    It does not need a "Finalize" button, as it is continuously linked
    :return: The number of paths, represented as a string (from the field)
    """
    global NUM_PATHS
    try:
        NUM_PATHS = int(num_paths) # We don't verify other aspects, assume it is true. Done by web-validation function
    except ValueError:
        return

START_TIME_DEFAULT:datetime.datetime = datetime.datetime.now()
START_TIME = START_TIME_DEFAULT
def select_depart_time(year:str, month:str, day:str, hour:str, minute:str):
    """
    Selects the starting time based on the user's selection of the time from the calendar/clock widget
    It represents the dynamic time held on the widget, set by default to the current time
    :param year: The selected year of calendar
    :param month: The selected month
    :param day: The clicked day
    :param hour: The scrolled hour
    :param minute: The minute
    :return: Creates and sets a datetime object representing the time understood by the application
    """
    global START_TIME
    START_TIME = datetime.datetime(int(year), list(calendar.month_abbr).index(month), int(day), int(hour), int(minute))

# Computation & Display

BEST_PATHS_DEFAULT:{[int]:(float, float, float)} = {}
BEST_PATHS = BEST_PATHS_DEFAULT
def submit_path_form():
    """
    Called when the [SUBMIT] button is called after all other fields have been entered.
    It will populate the PATHS_DETAILS Table, which should then be returned to the website.
    :return: A table of each path and its best qualities, in addition to tracing out all paths on the interactive map
    """
    global BEST_PATHS
    BEST_PATHS = Utils(USER).optimal_paths(START_TIME, START_NODE, END_NODE, NUM_PATHS)


# ADMIN PAGE

# The following Admin page methods already have Admin preferences as the user's preferences (every admin is a user)
# The preference creation method is already exemplified in the login separate "preferences" page

# OPTIMIZATION METRIC: Already set by user's preferences

ACTIONS_DEFAULT = []
ACTIONS = ACTIONS_DEFAULT
def add_action(coordinates:(float, float), gadget:str, add_or_remove:bool = True):
    """
    :param coordinates:
    :param gadget:
    :param add_or_remove:
    :return:
    """
    global ACTIONS
    feature = Gadget.LANE.parse(gadget, '') # Gadget.LANE is redundant caller
    add = [feature] if add_or_remove else []
    remove = [feature] if not add_or_remove else []
    ACTIONS += [Mutation(USER.curr_network, osmnx.nearest_edges(USER.curr_network, coordinates[0], coordinates[1]), add, remove, add_or_remove)]

# Recommender

SELECTED_BUDGET_DEFAULT = utils.Utils.NORMAL_BUDGET
SELECTED_BUDGET = SELECTED_BUDGET_DEFAULT
def select_budget(budget:str):
    """
    Called in the administrator webpage whenever the budget field is filled up
    If the input is not valid, then it adheres to the default selected budget
    :return: The interpreted considered budget
    """
    global SELECTED_BUDGET
    try:
        SELECTED_BUDGET = int(budget)
    except ValueError:
        return

SELECTED_NUM_RECOMMENDATIONS_DEFAULT = 1
SELECTED_NUM_RECOMMENDATIONS = SELECTED_NUM_RECOMMENDATIONS_DEFAULT
def select_recommendations(recommendations:str):
    """
    Called in the administrator webpage when the recommendations field is filled up, i.e. a new character is added
    Like the budget selection process, if the input is invalid, it adheres to the default selected recommendation number
    :param recommendations: The recommendation number filled up in the field
    :return: The number of selected recommendations
    """
    global SELECTED_NUM_RECOMMENDATIONS
    try:
        SELECTED_NUM_RECOMMENDATIONS = int(recommendations)
    except ValueError:
        return

COMPUTED_RECOMMENDATIONS_DEFAULT = []
COMPUTED_RECOMMENDATIONS = COMPUTED_RECOMMENDATIONS_DEFAULT
def compute_recommendations(recommendations:str):
    global COMPUTED_RECOMMENDATIONS
    COMPUTED_RECOMMENDATIONS = Utils(User()).best_predictions(SELECTED_BUDGET, SELECTED_NUM_RECOMMENDATIONS)

# Resetting all variables for convenience

def reset_user():
    """
    This is called either when the [RESET ALL] button is clicked on the user webpage, or when it is reloaded
    It then sets all parameters to their default values, so that the form can be rerun
    :return: Resets all parameters to their default values ONLY in the user webpage
    """
    global SELECTED_VEHICLE, SELECTED_ENVIRONMENT, PATH_METRIC, START_NODE, END_NODE, START_TIME
    global SELECTED_VEHICLE_DEFAULT, SELECTED_ENVIRONMENT_DEFAULT, PATH_METRIC_DEFAULT, START_NODE_DEFAULT, END_NODE_DEFAULT, START_TIME_DEFAULT
    SELECTED_VEHICLE = SELECTED_VEHICLE_DEFAULT
    SELECTED_ENVIRONMENT = SELECTED_ENVIRONMENT_DEFAULT
    PATH_METRIC = PATH_METRIC_DEFAULT
    START_NODE = START_NODE_DEFAULT
    END_NODE = END_NODE_DEFAULT
    START_TIME = START_TIME_DEFAULT

def reset_admin():
    """
    Called when the administrator clicks [RESET ALL] button to reset all fields to their default values, or reloads page
    Then sets all admin-related variables to their default values
    :return:
    """
    global ACTIONS, SELECTED_BUDGET, SELECTED_NUM_RECOMMENDATIONS, COMPUTED_RECOMMENDATIONS
    global ACTIONS_DEFAULT, SELECTED_BUDGET_DEFAULT, SELECTED_NUM_RECOMMENDATIONS_DEFAULT, COMPUTED_RECOMMENDATIONS_DEFAULT
    ACTIONS = ACTIONS_DEFAULT
    SELECTED_BUDGET = SELECTED_BUDGET_DEFAULT
    SELECTED_NUM_RECOMMENDATIONS = SELECTED_NUM_RECOMMENDATIONS_DEFAULT
    COMPUTED_RECOMMENDATIONS = COMPUTED_RECOMMENDATIONS_DEFAULT













