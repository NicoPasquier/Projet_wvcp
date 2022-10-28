import fileReader
import wvcp


name = "test"
nr_vertices = 4
nr_edges = 3
neighborhoods = [[1, 3], [0, 2], [1, 3], [0, 2]]
weight = [1, 1, 1, 1]
ub_colors = nr_vertices

name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./reduced_wvcp/miles500')

wvcp.wvcp(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors)
