def descendingSort(neighborhoods, weight):
    # Get index of sorted tab of weights 
    weight_sorted_index = sorted(range(len(weight)), key=lambda k: weight[k], reverse=True)
    # Get sorted tab of weights
    weight_sorted = sorted(weight, reverse=True)
    # Update of the neighborhoods
    new_neighborhoods = []
    for neighbors in neighborhoods:
        for i in range(len(neighbors)):
            new_vertice_value = weight_sorted_index.index(neighbors[i])
            neighbors[i] = new_vertice_value
    for i in range(len(weight_sorted_index)):
        new_neighborhoods.append(neighborhoods[weight_sorted_index[i]])

    return weight_sorted, new_neighborhoods