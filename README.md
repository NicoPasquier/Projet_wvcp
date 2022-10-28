# Projet_wvcp

Pour le lancement en ligne de commande (Python 3 est utilisé ici) il faut exécuter le fichier mainMutliFile.py avec la commande suivante :
    python mainMultiFile.py

Pour le dossier où se situe les graphes, modifier à la ligne 8 du fichier mainMultiFile.py "originals_graphs" par "reduced_wvcp" si vous souhaiter utiliser les graphs réduits.

La ligne 11 du fichier mainMultiFile.py applique un tri décroissant sur les poids des sommets (à l'aide du fichier sortWeights.py). Commentez cette ligne si vous utiliser les graphes réduits ou si vous ne voulez pas trier le poids des sommets.

Le fichier invoquer ligne 20 du fichier mainMultiFile.py contient les instances que l'on souhaite traiter. Mettez le fichier "instance_list_wvcp" si vous souhaitez traiter toute les instances disponible.

Lors de l'exécution du fichier mainMultiFile.py, un fichier results.csv contiendra le score et le temps des différentes instances traitées. 

Pour lancer simplement un seul fichier, il faut exécuter le fichier main.py en modifiant l'instance que vous souhaiter traiter ligne 12 avec la commande :
    python main.py

Vous pouvez commenter/décommenter les règles que vous souhaitez utilier (SR2, DR2) dans le fichier wvcp.py

Pour modifier l'affichage dans la console, commentez/décommentez ce que vous souhaitez dans la fonction "on_solution_callback(self)" du fichier wvcp_solutionPrinter.py

Pour le lancement avec plusieurs coeurs, modifiez la variable num_search_workers à la ligne 69 du fichier wvcp.py en y ajoutant le nombre de coeur que vous souhaitez utiliser. 