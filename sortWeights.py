# neighborhoods = [[1, 2, 8, 10, 13], [0, 2, 4, 14], [0, 1, 6, 9, 11], [4, 5, 6, 7, 12], [1, 3, 5, 6, 14], [3, 4, 6, 15], [2, 3, 4, 5, 9, 11], [3, 8, 9, 12], [0, 7, 9, 10, 13], [2, 6, 7, 8, 11], [0, 8, 11, 13], [2, 6, 9, 10], [3, 7, 13, 14, 15], [0, 8, 10, 12, 14, 15], [1, 4, 12, 13, 15], [5, 12, 13, 14]]
# weight = [5, 240, 50, 5, 85, 124, 5, 240, 85, 230, 124, 25, 50, 5, 230, 25]

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

    # print(weight_sorted_index)
    # print(weight_sorted)
    # print(neighborhoods)
    # print(new_neighborhoods)

    return weight_sorted, new_neighborhoods

# weight, neighborhoods = descendingSort(neighborhoods, weight)

# print(weight)
# print(neighborhoods)