from ortools.sat.python import cp_model
import time


class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, nr_vertices, arc, x, y, x_score):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__nr_vertices = nr_vertices
        self.__arc = arc
        self.__x = x
        self.__y = y
        self.__x_score = x_score
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count, self.Value(self.__x_score)

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution %i, time = %f s' %
              (self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1
        """print("x = [", end="")
        for i in range(len(self.__x)):
            print(self.__arc[i], "=> ", end="")
            print(self.Value(self.__x[i]), end=", ")
        print("]")"""
        print("y = ", self.Value(self.__y))
        print('score = %s' % self.Value(self.__x_score), end='\n\n')
