from fileReader import fileReader
from fileReader import sortWeights
from fileReader import transformGraph
from wvcp import wvcp_primal
from wvcp import wvcp_dual
from wvcp import wvcp_joint
import csv
import sys


def Solver(filename):
    # Get values
    name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/'+filename)

    # Descending sort
    weight, neighborhoods = sortWeights.descendingSort(neighborhoods, weight)

    # Solving
    score, optimal, time = wvcp_primal.primal(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors)

    return score, optimal, time


# header = ['Name', 'Number of Solutions','Score', 'Time (Seconds)']
header = ['Name', 'Score', 'Optimal', 'Time (Seconds)']

if __name__ == "__main__":
    file = ""
    rule = []
    thread = 1
    time_limit = 60
    lb_colors = 0
    ub_colors = None
    lb_score = None
    ub_score = None

    for argv in range(1, len(sys.argv)):
        if sys.argv[argv] == "-f" or sys.argv[argv] == "--file":
            file = sys.argv[argv+1]
        elif sys.argv[argv] == "-r" or sys.argv[argv] == "--rule":
            rule.append(sys.argv[argv+1])
        elif sys.argv[argv] == "-t" or sys.argv[argv] == "--thread":
            thread = int(sys.argv[argv+1])
        elif sys.argv[argv] == "-tl" or sys.argv[argv] == "--time_limit":
            time_limit = float(sys.argv[argv + 1])
        elif sys.argv[argv] == "--lb_colors":
            lb_colors = int(sys.argv[argv+1])
        elif sys.argv[argv] == "--ub_colors":
            ub_colors = int(sys.argv[argv+1])
        elif sys.argv[argv] == "--lb_score":
            lb_score = int(sys.argv[argv+1])
        elif sys.argv[argv] == "--ub_score":
            ub_score = int(sys.argv[argv+1])

    file = open("./annexes/test_instance_list.txt", "r")

    with open('./annexes/results.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in file:
            name = line.replace("\n", "")

            name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/' + name)

            # Descending sort
            weight, neighborhoods = sortWeights.descendingSort(neighborhoods, weight)

            # Solving
            score, optimal, time = wvcp_primal.primal(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, weight, lb_colors, ub_colors, lb_score, ub_score)
            writer.writerow([name+" (primal)", score, optimal, time])

            score, optimal, time = wvcp_dual.dual(thread, time_limit, name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_score, ub_score)
            writer.writerow([name + " (dual)", score, optimal, time])

            score, optimal, time = wvcp_joint.joint(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_colors, ub_colors, lb_score, ub_score)
            writer.writerow([name + " (joint)", score, optimal, time])

    file.close()
