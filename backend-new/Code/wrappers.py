from __future__ import annotations

import math

from Code.Accident.accident import Accident
from Code.Accident.outcome import Outcome


class AccidentWrapper:
    def __init__(self, instance:Accident):
        self.acc = instance

    def __eq__(self, other:AccidentWrapper):
        return self.acc.outcome == other.acc.outcome and self.acc.environment == other.acc.environment

    def __hash__(self):
        return hash(OutcomeWrapper(self.acc.outcome))*hash(self.acc.environment)

class OutcomeWrapper:
    def __init__(self, out:Outcome):
        self.out = out

    def __eq__(self, other:OutcomeWrapper):
        return self.out == other.out

    def __hash__(self):
        return math.prod([hash(veh)*math.prod([hash(elem) for elem in self.out.outcome[veh]]) for veh in self.out.outcome])

# Environment doesn't need to be wrapped, as it is subclass of hashable enum