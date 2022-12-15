from fileReader import fileReader
from fileReader import sortWeights
from fileReader import transformGraph
from wvcp import wvcp_primal
from wvcp import wvcp_dual

name = "test"
nr_vertices = 5
nr_edges = 5
neighborhoods = [[1, 2], [0], [0, 3, 4], [2, 4], [2, 3]]
weight = [1, 1, 2, 3, 1]

name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/p06')

print("Primal:")
wvcp_primal.primal(name, nr_vertices, nr_edges, neighborhoods, weight)

print("\n\nDual:")
wvcp_dual.dual(name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight)
