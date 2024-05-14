import csv

from DS.Atomic.gadget import Gadget
from DS.Atomic.vehicle import Vehicle
from DS.Structural.graph import Edge
from DS.Structural.section import Section
from DS.Structural.statistic import Statistic
from filenames import Filenames


def test():

    st = Statistic()
    cold = Filenames.collisiondata()
    mvol = Filenames.midblockvols()[2023]
    ivol = Filenames.intersectvols()[2023]
    cent = Filenames.centrelines()

    with open(cold) as coll:
        rdr = csv.reader(coll)
        collisions = [line for line in rdr][-10:]

    with open(mvol) as mid:
        rdr = csv.reader(mid)
        mvolumes = [line for line in rdr][1:]

    with open(ivol) as ins:
        rdr = csv.reader(ins)
        ivolumes = [line for line in rdr][1:]
    st.extract(collisions, mvolumes, ivolumes, 2023, 2023, 9000)

    gadgets = [Gadget.CAMERA, Gadget.STOPLIGHT]
    s = Section(st, gadgets)
    print(s.stats.times[Vehicle.CAR])
    s.modify(Gadget.CROSSOVER)
    print(s.stats.times[Vehicle.CAR])

    with open(cent) as cns:
        rdr = csv.reader(cns)
        first = True
        for line in rdr:
            if not first:
                a, b = Edge().parse(cent, line)
                print(a)
                print(b)
            first = False








if __name__ == '__main__':
    test()
