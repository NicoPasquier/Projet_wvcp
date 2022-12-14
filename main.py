import fileReader
import wvcp
import transformGraph
import wvcp_dual

name = "test"
nr_vertices = 5
nr_edges = 5
neighborhoods = [[1, 2], [0], [0, 3, 4], [2, 4], [2, 3]]
weight = [1, 1, 2, 3, 1]
name = "test"
nr_vertices = 4
nr_edges = 3
neighborhoods = [[1], [0, 2], [1, 3], [2]]
weight = [1, 2, 3, 4]
ub_colors = nr_vertices


name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/p06')

#print(transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight))
wvcp_dual.dual(name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight)

wvcp.wvcp(name, nr_vertices, nr_edges, neighborhoods, weight, nr_vertices)
