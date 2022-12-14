import fileReader

def genComplementaryGraph(nr_vertices, neighborhoods, weight):

    compGraph = []

    # First create the non-oriented graph 
    for i in range(nr_vertices):
        successors = []
        current = neighborhoods[i]
        for j in range(nr_vertices):
            if (j not in current) & (j != i):
                successors.append(j)
        compGraph.append(successors)

    # Then generate the oriented graph
    for i in range(nr_vertices):
        current = compGraph[i]
        for j in current:
            successors = compGraph[j]
            if (weight[i] >= weight[j]):
                if (i in successors):
                    successors.remove(i)
            else:
                if (j in successors):
                    successors.remove(j)

    return(compGraph)

    

# nr_vertices = 5
# neighborhoods = [[1,2], [0], [0,3,4], [2,4], [2,3]]
# weight = [1,1,2,3,1]

# print(neighborhoods)

# newGraph = genComplementaryGraph(nr_vertices, neighborhoods, weight)

# print(newGraph)

# name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/'+"p06")

# print(neighborhoods)
# compGraph = genComplementaryGraph(nr_vertices, neighborhoods, weight)
# print(compGraph)