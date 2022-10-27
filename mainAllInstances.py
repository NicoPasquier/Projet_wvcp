import fileReader
import wvcp
import sortWeights
import csv

def Solver(filename):
    # Get values
    name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/'+filename)

    # Descending sort
    weight, neighborhoods =  sortWeights.descendingSort(neighborhoods, weight)

    # Solving
    count, score, time = wvcp.wvcp(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors)

    return count, score, time

header = ['Name', 'Number of Solutions','Score', 'Time (Seconds)']
data = []

file = open("test_instance_approuved.txt", "r")

with open('results.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for line in file:
        name = line.replace("\n", "")
        count, score, time = Solver(name)
        writer.writerow([name, count, score, time])

file.close()