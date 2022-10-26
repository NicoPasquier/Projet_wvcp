from ortools.sat.python import cp_model
import time


class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, nr_vertices, nr_edges, neighborhoods, x_color, y_color, x_weight, x_score, ub_color):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__nr_vertices = nr_vertices
        self.__nr_edges = nr_edges
        self.__neighborhoods = neighborhoods
        self.__x_color = x_color
        self.__y_color = y_color
        self.__x_weight = x_weight
        self.__x_score = x_score
        self.__ub_color = ub_color
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution %i, time = %f s' %
              (self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1

        self.affichage_Matrice()
        print()
        self.affichage_Sommet_Couleur()
        print()
        self.affichage_Poids_Couleur()
        print()
        print('score = %s' % self.Value(self.__x_score), end='\n\n')

    def affichage_Matrice(self):
        for i in range(self.__nr_vertices):
            for j in range(self.__ub_color):
                print('%i' % self.Value(self.__x_color[i, j]), end=' ')
            print()

    def affichage_Sommet_Couleur(self):
        """for i in range(self.__nr_vertices):
            for j in range(self.__ub_color):
                if self.Value(self.__x_color[i, j]) == 1:
                    print('sommet %i = %f' % (i, j))"""
        for i in range(self.__nr_vertices):
            print('sommet %i = %f' % (i, self.Value(self.__y_color[i])))

    def affichage_Poids_Couleur(self):
        print('poids des couleur: [', end='')
        for i in range(self.__ub_color):
            print('%i' % self.Value(self.__x_weight[i]), end=' ')
        print(']', end='\n')
