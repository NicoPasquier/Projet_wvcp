from ortools.sat.python import cp_model
import wvcp_solutionPrinter


def wvcp(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors):
    print(name + '\n')

    model = cp_model.CpModel()

    x_color = {}
    for i in range(2 * nr_vertices):
        for j in range(ub_colors):
            x_color[(i, j)] = model.NewIntVar(0, 1, 'vertices%i color%f' % (i, j))

    x_weight = [model.NewIntVar(0, max(weight), 'color%i' % i) for i in range(ub_colors)]
    x_score = model.NewIntVar(0, sum(weight), 'score')

    for i in range(2 * nr_vertices):
        model.Add((sum(x_color[i, j] for j in range(ub_colors))) == 1)

    for i1 in range(nr_vertices):
        for i2 in neighborhoods[i1]:
            for j in range(ub_colors):
                model.Add(x_color[i1, j] + x_color[i2, j] <= 1)

    for j in range(ub_colors):
        model.AddMaxEquality(x_weight[j], (x_color[i, j] * weight[i] for i in range(nr_vertices)))

    model.Add(x_score == sum(x_weight))
    model.Minimize(x_score)

    solver = cp_model.CpSolver()
    solution_printer = wvcp_solutionPrinter.SolutionPrinter(nr_vertices, nr_edges, neighborhoods, x_color, x_weight, x_score, ub_colors)
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.Solve(model, solution_printer)
