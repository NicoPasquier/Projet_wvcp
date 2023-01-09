import sys

from fileReader import fileReader
from fileReader import sortWeights
from fileReader import transformGraph
from wvcp import wvcp_primal
from wvcp import wvcp_dual
from wvcp import wvcp_joint


def help():
    s = "Pour le lancement en ligne de commande (Python 3 est utilisé ici) il faut exécuter le fichier main.py avec la commande suivante :\n\tpython3 main.py [option]...\nLes options sont:\n\t-m, --method [primal|dual|joint]: indiquer la méthode souhaiter parmis primal, dual ou joint\n\t-f, --file [fichier]: indiquer où se situe le fichier de l'instances qu'on souhaite tester\n\t-r, --rule [SR2|DR2]: choisir la règle SR2 ou DR2\n\t-t, --thread [nb de thread]: choisir le nombre de thread \n\t-tl, --time_limit [limite de temps]: choisir la limite de temps pour chaque instance\n\t--lb_colors [lb_colors]: choisir la borne inférieur pour la couleur\n\t--ub_colors [ub_colors]: choisir la borne supérieur pour la couleur\n\t--lb_score [lb_score]: choisir la borne inférieur pour le score\n\t--ub_score [ub_score]: choisir la borne supérieur pour le score\n\t-h, --help: affiche l'aide\n\nPour modifier l'affichage dans la console, commentez/décommentez ce que vous souhaitez dans la fonction \"on_solution_callback(self)\" du fichier wvcp_solutionPrinter.py"
    print(s)


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
        elif sys.argv[argv] == "-h" or sys.argv[argv] == "--help":
            help()

    if file != "":
        name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader(file)
        # Descending sort
        weight, neighborhoods = sortWeights.descendingSort(neighborhoods, weight)

        if "primal" in method:
            print("Primal:")
            score, optimal, time = wvcp_primal.primal(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, weight, lb_colors, ub_colors, lb_score, ub_score)
            print("Optimal=" + str(optimal))
        if "dual" in method:
            print("Dual:")
            score, optimal, time = wvcp_dual.dual(thread, time_limit, name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_score, ub_score)
            print("Optimal=" + str(optimal))
        if "joint" in method:
            print("Joint:")
            score, optimal, time = wvcp_joint.joint(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_colors, ub_colors, lb_score, ub_score)
            print("Optimal=" + str(optimal))
