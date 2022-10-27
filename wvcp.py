from ortools.sat.python import cp_model

import cp_sat_utils
import wvcp_solutionPrinter


def wvcp(name, nr_vertices, nr_edges, neighborhoods, weight, ub_colors):
    print(name + '\n')

    model = cp_model.CpModel()

    x_color = {}
    for i in range(nr_vertices):
        for j in range(ub_colors):
            x_color[(i, j)] = model.NewIntVar(0, 1, 'vertices%i color%f' % (i, j))

    y_color = [model.NewIntVar(0, ub_colors, 'sommet%i' % i)for i in range(nr_vertices)]
    x_weight = [model.NewIntVar(0, max(weight), 'color%i' % i) for i in range(ub_colors)]
    x_score = model.NewIntVar(0, sum(weight), 'score')

    for i in range(nr_vertices):
        model.Add((sum(x_color[i, j] for j in range(ub_colors))) == 1)

    for i in range(nr_vertices):
        for j in range(ub_colors):
            b = model.NewBoolVar("")
            model.Add(x_color[i, j] == 1).OnlyEnforceIf(b)
            model.Add(x_color[i, j] == 0).OnlyEnforceIf(b.Not())
            model.Add(y_color[i] == j).OnlyEnforceIf(b)
            model.Add(y_color[i] != j).OnlyEnforceIf(b.Not())

    for i1 in range(nr_vertices):
        for i2 in neighborhoods[i1]:
            for j in range(ub_colors):
                model.Add(x_color[i1, j] + x_color[i2, j] <= 1)

    for j in range(ub_colors):
        model.AddMaxEquality(x_weight[j], (x_color[i, j] * weight[i] for i in range(nr_vertices)))

    cp_sat_utils.decreasing(model, x_weight)

    # SR1

    # DR1

    # SR2
    for i in range(nr_vertices):
        model.Add(y_color[i] <= len(neighborhoods[i]) + 1)

    # DR2
    for i in range(nr_vertices):
        z = [model.NewIntVar(0, len(neighborhoods[i]), '%i' % j) for j in range(nr_vertices+1)]
        cp_sat_utils.global_cardinality(
            model,
            [y_color[u] for u in neighborhoods[i]],
            [j for j in range(nr_vertices+1)],
            z
        )
        model.Add(y_color[i] == cp_sat_utils.argmin(model, z))

    model.Add(x_score == sum(x_weight))
    model.Minimize(x_score)

    solver = cp_model.CpSolver()
    solution_printer = wvcp_solutionPrinter.SolutionPrinter(nr_vertices, nr_edges, neighborhoods, x_color, y_color, x_weight, x_score, ub_colors)
    solver.parameters.enumerate_all_solutions = True
    #solver.parameters.num_search_workers = 4
    solver.Solve(model, solution_printer)
