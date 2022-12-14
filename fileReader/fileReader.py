def fileReader(filename):
    name = filename

    file = open(filename+'.col.w', "r")
    nr_vertices = 0
    weight = []
    for line in file:
        weight.append(int(line))
        nr_vertices += 1
    file.close()

    file = open(filename+'.edgelist', "r")
    nr_edges = 0
    neighborhoods = [[] for i in range(nr_vertices)]
    for line in file:
        aux = line.replace("\n", "").split(" ")
        neighborhoods[int(aux[0])].append(int(aux[1]))
        neighborhoods[int(aux[1])].append(int(aux[0]))
        nr_edges += 1
    file.close()

    ub_colors = nr_vertices

    return name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors
