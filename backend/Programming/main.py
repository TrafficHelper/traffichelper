import csv

import application

# def load():
#     # Step 1 - Load all Traffic Networks
#     fn = application.Filenames.centrelines() # The str pathname of the centre lines file
#     nodes = application.Node().parse(fn, []) # Dummy variables as node already parses such data
#     edgesOutID: {str:[]} = {} # Dict of Edges sorted by the identity of the other Edge they emerge from
#     edgesInID: {str:[]} = {} # Dict of Edges sorted by the identity of the other Edge they go into
#     with open(fn) as structure:
#         rdr = csv.reader(structure)
#         for line in rdr:
#             left, right = application.Edge().parse(fn, line)
#             edgesOutID[left.fromID] += left
#             edgesOutID[right.fromID] += right
#             edgesInID[left.toID] += left
#             edgesInID[right.toID] += right
#
#             edges += application.Edge().parse(fn, line)  # Parse each set of edges
#
#
#     edges = application.Edge().parse(application.Filenames.centrelines(), [])
#
# def run():
#     vehicles = Vehicle().parse()

def edgeloaderTest():
    edges = []
    fn = application.Filenames.centrelines()
    with open(fn) as structure:
        rdr = csv.reader(structure)
        for line in rdr:
            edges += application.Edge().parse(fn, line)
    return edges


if __name__ == '__main__':
    result = edgeloaderTest()
    print(result)
    run()

