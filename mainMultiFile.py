from fileReader import fileReader
from fileReader import sortWeights
from fileReader import transformGraph
from wvcp import wvcp_primal
from wvcp import wvcp_dual
from wvcp import wvcp_joint
import csv
import sys


def help():
    s = "Pour le lancement en ligne de commande (Python 3 est utilisé ici) il faut exécuter le fichier mainMutliFile.py avec la commande suivante :\n\tpython3 mainMultiFile.py [option]...\nLes options sont:\n\t-m, --method [primal|dual|joint]: indiquer la méthode souhaiter parmis primal, dual ou joint\n\t-f, --file [fichier]: indiquer où se situe le fichier avec les instances qu'on souhaite tester\n\t-r, --rule [SR2|DR2]: choisir la règle SR2 ou DR2\n\t-t, --thread [nb de thread]: choisir le nombre de thread \n\t-tl, --time_limit [limite de temps]: choisir la limite de temps pour chaque instance\n\t--lb_colors [lb_colors]: choisir la borne inférieur pour la couleur\n\t--ub_colors [ub_colors]: choisir la borne supérieur pour la couleur\n\t--lb_score [lb_score]: choisir la borne inférieur pour le score\n\t--ub_score [ub_score]: choisir la borne supérieur pour le score\n\t-h, --help: affiche l'aide\n\nPour le dossier où se situe les graphes, modifier à la ligne 64 et 65 du fichier mainMultiFile.py \"originals_graphs\" par \"reduced_wvcp\" si vous souhaiter utiliser les graphs réduits.\n\nLa ligne 68 du fichier mainMultiFile.py applique un tri décroissant sur les poids des sommets (à l'aide du fichier sortWeights.py). Commentez cette ligne si vous utiliser les graphes réduits ou si vous ne voulez pas trier le poids des sommets.\n\nLors de l'exécution du fichier mainMultiFile.py, un fichier results.csv contiendra le score et le temps des différentes instances traitées."
    print(s)


def Solver(filename):
    # Get values
    name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/'+filename)
    # name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./reduced_wvcp/'+filename)

    # Descending sort
    weight, neighborhoods = sortWeights.descendingSort(neighborhoods, weight)

    # Solving
    score, optimal, time = wvcp_primal.primal(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors)

    return score, optimal, time


# header = ['Name', 'Number of Solutions','Score', 'Time (Seconds)']
header = ['Name', 'Score', 'Optimal', 'Time (Seconds)']

if __name__ == "__main__":
    file = ""
    method = []
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
        elif sys.argv[argv] == "-h" or sys.argv[argv] == "--help":
            help()

    file = open("./annexes/test_instance_list.txt", "r")

    with open('./annexes/results.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in file:
            name = line.replace("\n", "")

            name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./original_graphs/' + name)
            # name, nr_vertices, weight, nr_edges, neighborhoods, ub_colors = fileReader.fileReader('./reduced_wvcp/'+filename)

            # Descending sort
            weight, neighborhoods = sortWeights.descendingSort(neighborhoods, weight)

            # Solving
            if "primal" in method:
                score, optimal, time = wvcp_primal.primal(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, weight, lb_colors, ub_colors, lb_score, ub_score)
                writer.writerow([name+" (primal)", score, optimal, time])

            if "dual" in method:
                score, optimal, time = wvcp_dual.dual(thread, time_limit, name, nr_vertices, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_score, ub_score)
                writer.writerow([name + " (dual)", score, optimal, time])

            if "joint" in method:
                score, optimal, time = wvcp_joint.joint(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, transformGraph.genComplementaryGraph(nr_vertices, neighborhoods, weight), weight, lb_colors, ub_colors, lb_score, ub_score)
                writer.writerow([name + " (joint)", score, optimal, time])

    file.close()
