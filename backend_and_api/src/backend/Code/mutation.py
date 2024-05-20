import itertools

import networkx
import osmnx
from networkx import MultiDiGraph

from backend.Code import loader
from backend.Code.Atomic.gadget import Gadget
from backend.Code.Interfaces.cost import Cost


class Mutation(Cost):

    """
    Class representing a Mutation, or a series of actions which may be undertaken on the graph
    A Mutation consists of a series of additions or removals of a list of Gadget
    Alternatively, it consists of taking in or out an entire section, in which case the above is pointless
    A Mutation consists of:
        - section:int --> The edge identity of the networkx traffic network
        - additions:[Gadget] --> The list of gadgets being added to the edge
        - removals:[Gadget] --> The list of gadgets being removed from the edge
        - shift:bool = False --> An optional parameter whether to add or remove an edge, only called if the additions or removals are empty
    """

    def __init__(self, graph:MultiDiGraph, section:(int, int, int), additions:[Gadget], removals:[Gadget], add_or_remove:bool = False):
        self.network = graph
        self.target = section
        self.additions = additions
        self.removals = removals
        # We don't consider modifying the network if there are some additions or removals; the shift parameter is then redundant
        self.add_or_remove = add_or_remove if len(additions) == 0 == len(removals) else False
        print(add_or_remove)

    def is_section_modifier(self):
        return len(self.additions) == 0 == len(self.removals)

    def __str__(self):
        """
        Returns the string representation of this Modification sequence.
        The string representation is how this object will be represented, oftentimes in the CLI too.
        If the action is merely an addition or removal, it will display such
        Otherwise it will specify the section along with the additions or removals to that section
        :return:
        """
        if self.is_section_modifier():
            return 'Added ' if self.add_or_remove else 'Removed ' + str(self.target) + ' against network'
        else:
            return 'Section: '+str(self.target)+', added:'+str(self.additions)+', removed:'+str(self.removals)

    def apply(self, refactor:bool = False) -> [bool]:
        """
        Applies this modification to the road network and optionally computes the ramifications
        It applies all the additions first and then the removals, by default
        Returns a trace on whether each REMOVAL was successfully completed, or it was insufficient, in this case it is order-dependent
        :param refactor: Modify parameters on the network based on the prediction if True, simply add them if False
        :return: Mutates the graph accordingly and returns the work trace
        """
        trace = []
        u, v, key = (self.target[i] for i in [0, 1, 2])
        if not refactor:
            if self.is_section_modifier(): # If adding or removing an edge, all other terms are redundant
                if self.add_or_remove:
                    self.network.add_edge(u, v, key)
                else:
                    self.network.remove_edge(u, v, key)
            else:
                trace = self.treat_add_gadgets()
            return trace
        else:
            if self.is_section_modifier(): # If adding or removing an empty edge devoid of all other terms
                if self.add_or_remove: # Want to add feature
                    self.redistribute(True)
                else:
                    self.redistribute(False)
            else: # Simple addition and removal of gadget sequence with refactoring, we should decrease number of accidents through addition and removal of particular gadgets
                self.treat_add_gadgets(True) # Just add the gadgets
                # Adding another lane will decrease the risk of accidents proportional to the number of lanes; n lanes give 1/n the amount of accidents in all weather
                # A speed increase of 5 kmh will increase the accidents according to a sigmoid % of the initial computed result
                # A stoplight will halve the risk of an accident
                # A speed enforcer will 0.8x the risk of an accident

    def treat_add_gadgets(self, refactor=False):
        """
        :param refactor: Whether to dynamically refactor the network as gadgets are added and removed
        :return: Adds and removes the given set of addition and removal of gadgets to the network and returns a stack trace on whether each one could be completed
        """
        for added_gadget in self.additions: # Add all listed gadgets
            curr_data = loader.deserialize(networkx.get_edge_attributes(self.network, 'gadgets')[self.target], False)
            curr_data[added_gadget] += 1
            networkx.set_edge_attributes(self.network, {self.target:curr_data}, 'gadgets')
            if refactor:
                self.compute_changed_gadget(added_gadget, True)

        # Remove specified gadgets
        n = len(self.removals)
        trace = [True] * n
        for i in range(n):
            removed_gadget = self.removals[i]
            curr_data = loader.deserialize(networkx.get_edge_attributes(self.network, 'gadgets')[self.target], False)
            if curr_data[removed_gadget] == 0: # Cannot remove nonexistent gadget
                trace[i] = False
            else:
                curr_data[removed_gadget] -= 1
                trace[i] = True
                if refactor:
                    self.compute_changed_gadget(removed_gadget, False)
        return trace

    division = lambda data, avg: {veh:data[veh]/avg for veh in data} # Dividing a list of vehicles by a value
    addition = lambda data: {sum(data[i][j]) for i in data for j in data[i]} # The sum of all lists of vehicles
    negation = lambda data: {veh:-data[veh] for veh in data} # The negation of the list, temporary convenience for subtraction

    def redistribute(self, add_or_remove:bool = True):
        """
        Redistributes traffic flow upon adding or removing the section from the network (add_or_remove is true or false, respectively).
        We can visualize the one-way segment as of the form <--> A --> B <--> where <--> denotes a complex of incoming and outgoing edges
        True to the conservation of flow:
        - When adding, each of A's outgoing edges will drop a little to contribute to Edge: A --> B. Similarly, B's outgoing edges will increase uniformly by some amount
        - When subtracting an edge, the reverse of this process should occur. B out edges should decrement by half of its flow, and A edges should be increased by the flow value divided by their number
        The flows redistribution policy must conform to the two following postulates:
        - Conservation of flow: The total flow in the network before and after an addition must be the same
        - Reversibility of distribution: The flow distribution after reversing a series of changes must be exactly the same as before they were added
        While these are not completely accurate descriptions of reality, they serve a useful approximation
        Incidentally, flow is NOT impacted by any gadget change for these purposes, as is also experimentally demonstrated
        :param add_or_remove: Compute dynamics based on adding or removing a route
        :return: Refactor the flows to account for the addition or removal
        """

        # Add key with default loader template
        print(self.target)
        u, v, key = self.target

        # Edges of relevant interest
        edges = self.network.edges
        print(networkx.get_edge_attributes(edges))
        exit()
        u_out_edges = networkx.get_edge_attributes(self.network, self.network.out_edges(u), 'flow')
        nu = len(u_out_edges)
        print(nu)
        v_out_edges = networkx.get_edge_attributes(self.network, self.network.out_edges(v), 'flow')
        nv = len(v_out_edges)
        print(nv)
        # u_out_edges = {ou:edges[ou['flows']] for ou in self.network.out_edges(u)}
        # nu = len(u_out_edges)
        # v_out_edges = {ov:edges[ov['flows']] for ov in self.network.out_edges(v)}
        # nv = len(v_out_edges)

        print(add_or_remove)
        if add_or_remove: # Adding an edge
            print('hello')
            self.network.add_edge(u, v, key)
            if nu == 0 or nv == 0: # Either the start or end has no influential edges, so this will also be empty with no impact
                return # It will have no flow and influence nothing here
            # Equally distribute each flow from each of the nu u_out_edges to this edge
            print(u_out_edges)
            leaving = {edge:Mutation.division(u_out_edges[edge], nu) for edge in u_out_edges} # Each out edge from u contributes (lacks) proportional to itself
            half_amount = Mutation.division(Mutation.addition(leaving.values()), 2) # The amount which should be added to this edge
            # The outgoing nv v_out edges will also need an even distribution of amount added to them
            nv_increment = Mutation.division(half_amount, nv) # So this is that amount which will be incremented
            # In conclusion ...
            networkx.set_edge_attributes(self.network, {self.target:half_amount}, 'flows') # We set the flow of the edge
            # ... and Increment edge by distribution
            networkx.set_edge_attributes(self.network, {out:Mutation.addition([v_out_edges[out], nv_increment]) for out in v_out_edges}, 'flows') # ... and increment each out edge by the distribution
        else: # Removing an edge
            insurance_edge = osmnx.nearest_edges(self.network, 45.5, 75.5) # Random position to get from, will arbitrarily be added with flow in case of pathological case
            this_flow = self.network.remove_edge(u, v, key)['flows'] # The HALF amount of flow which should have been accorded
            nu -= 1 # One less u out edge from removing this edge
            if nu == 0 or nv == 0: # For same reason as above, there will exist no other out edge
                # But we have to distribute its flow, so ... in this pathological highly unlikely (unless the data is inconsistent) case, arbitrarily distribute it to all edges except it at random
                # Efficient: Choose arbitrary edge and increment its flow by that much
                data = Mutation.addition(networkx.get_edge_attributes(self.network, insurance_edge, 'flows'))
                networkx.set_edge_attributes({insurance_edge:data}, 'flows') # Temporary
                return # If nu == 0, then there are only in edges, which have prior been modified, sink. Similar for nv == 0, also sink. This is not possible to change flow, cannot appear out of nowhere
            decrement_amount = Mutation.division(this_flow, nv) # The amount to decrease each nv by
            # Then we decrement each out edge by our decrement indicator, returning them to their original
            networkx.set_edge_attributes({out:Mutation.addition([v_out_edges[out], Mutation.negation(decrement_amount)]) for out in v_out_edges}, 'flows')
            # Set all edges to their previously expected values, flow does not change
            networkx.set_edge_attributes(self.network, {out_u: Mutation.division(u_out_edges[out_u], 1 - 1/nu) for out_u in u_out_edges}, 'flows')

    # Repeat the list of accidents until a given factor is reached
    trim = lambda accidents, factor: accidents[:int(len(accidents)*factor)] if factor < 1 else list(itertools.islice(itertools.cycle(accidents), int(factor*len(accidents))))

    def compute_changed_gadget(self, gadget:Gadget, add_or_remove:bool): # TODO Fix impact of changed gadgets
        """
        Computes the effect of adding or removing the changed Gadget on the network
        Assume the network already has the Gadget added to it or removed from it.
        :param gadget: The gadget being added or removed
        :param add_or_remove: Whether to add or remove
        :return: Refactors the network's data accordingly
        """

        # Risk is influenced by trimming accidents
        # Travel time is influenced by speed
        # Distance remains the same for any gadget addition

        speed = float(networkx.get_edge_attributes(self.network, 'speed_kph')[self.target])
        accident = networkx.get_edge_attributes(self.network, 'accidents')[self.target]

        # Change matrix:
        if gadget == Gadget.LANE:
            accident = Mutation.trim(accident, 0.8) # Adding a lane decreases accident risk by 20%
            # Other parameters aren't influenced by adding another lane, for this application

        if gadget == Gadget.SPEED_INCREASE:
            speed += 10 # Speed increase block size
            accident = Mutation.trim(accident, 2) # Accidents double for every 10kmh above speed limit

        if gadget == Gadget.STOP_LIGHT:
            accident = Mutation.trim(accident, 0.7) # Increasing lane decreases accident risk by 30%
            speed -= 3 # Equivalent time decreases by 30 seconds, so about 3kmh

        if gadget == Gadget.SPEED_ENFORCER:
            accident = Mutation.trim(accident, 0.5) # Accidents decrease too here

        # Set new speed, and accidents. From speed, travel time will be computed, and from accidents, risk will be. Then both will be combined to compute new cost of network
        networkx.set_edge_attributes(self.network, {self.target:speed}, 'speed_kph')
        networkx.set_edge_attributes(self.network, {self.target:accident}, 'accidents')
        osmnx.add_edge_travel_times(self.network)
        loader.compute_risks(self.network)
        loader.compute_costs(self.network)





