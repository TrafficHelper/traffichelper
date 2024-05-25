import datetime

import osmnx

from Code.Accident.environment import Environment
from Code.Atomic.vehicle import Vehicle
from Code.Utils.preferences import Preferences
from Code.Utils.utils import Utils
from Code.user import User

me = User()
tool = Utils(me)
me.preferences = Preferences(Vehicle.TRUCK, Environment.DEVIANT, (1/3, 1, 1/2))

start_address = '2 Sheldrake Drive, Ottawa, Canada'
start_lat, start_long = osmnx.geocode(start_address)

end_address = '1755 Merivale Road, Ottawa, Canada'
end_lat, end_long = osmnx.geocode(end_address)

number_paths = 10

best_paths = tool.optimal_paths(datetime.datetime.now(), (start_lat, start_long), (end_lat, end_long), number_paths)
for path in best_paths:
    print(str(path) + ':' + str(best_paths[path]))
tool.print_paths(best_paths)




