import sys

from fileReader import fileReader
from fileReader import sortWeights
from fileReader import transformGraph
from wvcp import wvcp_primal
from wvcp import wvcp_dual
from wvcp import wvcp_joint


if __name__ == "__main__":
    method = []
    file = ""
    rule = []
    thread = 1
    time_limit = 60
    lb_colors = 0
    ub_colors = None
    lb_score = None
    ub_score = None

    for argv in range(1, len(sys.argv)):
        if sys.argv[argv] == "-m" or sys.argv[argv] == "--method":
            method.append(sys.argv[argv+1])
        elif sys.argv[argv] == "-f" or sys.argv[argv] == "--file":
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

    name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader(file)

    if "primal" in method:
        print("Primal:")
        wvcp_primal.primal(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, weight, lb_colors, ub_colors, lb_score, ub_score)
    if "dual" in method:
        print("Dual:")
        wvcp_dual.dual(thread, time_limit, name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_score, ub_score)
    if "joint" in method:
        print("Joint:")
        wvcp_joint.joint(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_colors, ub_colors, lb_score, ub_score)
