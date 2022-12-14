from ortools.sat.python import cp_model
from ortools.sat import sat_parameters_pb2
import wvcp_dual_solutionPrinter


def dual(name, nr_vertices, arc, weight):
    print(name + '\n')

    model = cp_model.CpModel()

    x = [model.NewIntVar(0, 1, "x%i%f" % (i[0], i[1]))for i in arc]
    y_weight = [model.NewIntVar(0, max(weight), "weight%i" % i)for i in range(len(arc))]
    y = model.NewIntVar(0, sum(weight), 'y')
    x_score = model.NewIntVar(0, sum(weight), 'score')

    for i in range(len(arc)):
        for j in range(i+1, len(arc)):
            if arc[i][0] == arc[j][0] and not((arc[i][1], arc[j][1]) in arc) and not((arc[j][1], arc[i][1]) in arc):
                model.Add(x[i] + x[j] <= 1)
            if arc[i][0] == arc[j][1] or arc[i][1] == arc[j][0]:
                model.Add(x[i] + x[j] <= 1)
            if arc[i][1] == arc[j][1]:
                model.Add(x[i] + x[j] <= 1)

    for i in range(len(arc)):
        model.Add(y_weight[i] == x[i] * weight[arc[i][1]])

    model.Add(y == sum(y_weight))

    model.Add(x_score == sum(weight)-y)

    #model.AddDecisionStrategy(x, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_LOWER_HALF)
    model.Minimize(x_score)

    solver = cp_model.CpSolver()
    solution_printer = wvcp_dual_solutionPrinter.SolutionPrinter(nr_vertices, arc, x, y,x_score)
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 4
    solver.parameters = sat_parameters_pb2.SatParameters(num_search_workers=4)
    solver.Solve(model, solution_printer)
    count, score = solution_printer.solution_count()
    time = solver.WallTime()
    print(time)

    return count, score, time
