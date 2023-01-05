from ortools.sat.python import cp_model
import time

class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, nr_vertices, nr_edges, neighborhoods, x_color, y_color, x_weight, x_dominant=None, x_score=None, ub_color=None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__nr_vertices = nr_vertices
        self.__nr_edges = nr_edges
        self.__neighborhoods = neighborhoods
        self.__x_color = x_color
        self.__y_color = y_color
        self.__x_weight = x_weight
        self.__x_dominant = x_dominant
        self.__x_score = x_score
        self.__ub_color = ub_color
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count, self.Value(self.__x_score)

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution %i, time = %f s' %
              (self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1
        print('score = %s' % self.Value(self.__x_score), end='\n\n')