# Projet_wvcp

Pour le lancement en ligne de commande (Python 3 est utilisé ici) il faut exécuter le fichier mainMutliFile.py avec la commande suivante :
    python3 mainMultiFile.py [option]...

Les options sont:
	-m, --method [primal|dual|joint]: indiquer la méthode souhaiter parmis primal, dual ou joint
	-f, --file [fichier]: indiquer où se situe le fichier avec les instances qu'on souhaite tester	
	-r, --rule [SR2|DR2]: choisir la règle SR2 ou DR2
	-t, --thread [nb de thread]: choisir le nombre de thread 
	-tl, --time_limit [limite de temps]: choisir la limite de temps pour chaque instance
	--lb_colors [lb_colors]: choisir la borne inférieur pour la couleur
	--ub_colors [ub_colors]: choisir la borne supérieur pour la couleur
	--lb_score [lb_score]: choisir la borne inférieur pour le score
	--ub_score [ub_score]: choisir la borne supérieur pour le score
	-h, --help: affiche l'aide

Pour le dossier où se situe les graphes, modifier à la ligne 64 et 65 du fichier mainMultiFile.py "originals_graphs" par "reduced_wvcp" si vous souhaiter utiliser les graphs réduits.

La ligne 68 du fichier mainMultiFile.py applique un tri décroissant sur les poids des sommets (à l'aide du fichier sortWeights.py). Commentez cette ligne si vous utiliser les graphes réduits ou si vous ne voulez pas trier le poids des sommets.

Lors de l'exécution du fichier mainMultiFile.py, un fichier results.csv contiendra le score et le temps des différentes instances traitées. 

Pour lancer simplement un seul fichier, il faut exécuter le fichier main.py en modifiant l'instance que vous souhaiter traiter ligne 12 avec la commande :
    python3 main.py [option]...

Les options sont:
	-m, --method [primal|dual|joint]: indiquer la méthode souhaiter parmis primal, dual ou joint
	-f, --file [fichier]: indiquer où se situe le fichier de l'instances qu'on souhaite tester
	-r, --rule [SR2|DR2]: choisir la règle SR2 ou DR2
	-t, --thread [nb de thread]: choisir le nombre de thread 
	-tl, --time_limit [limite de temps]: choisir la limite de temps pour chaque instance
	--lb_colors [lb_colors]: choisir la borne inférieur pour la couleur
	--ub_colors [ub_colors]: choisir la borne supérieur pour la couleur
	--lb_score [lb_score]: choisir la borne inférieur pour le score
	--ub_score [ub_score]: choisir la borne supérieur pour le score
	-h, --help: affiche l'aide

Pour modifier l'affichage dans la console, commentez/décommentez ce que vous souhaitez dans la fonction "on_solution_callback(self)" du fichier wvcp_solutionPrinter.py

