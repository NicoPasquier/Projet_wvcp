from ortools.sat.python import cp_model
from ortools.sat import sat_parameters_pb2

from . import cp_sat_utils
from . import wvcp_globals
from . import wvcp_primal_solutionPrinter


def primal(name, nr_vertices, nr_edges, neighborhoods, weight, lb_colors=0, ub_colors=None, lb_score=None, ub_score=None):
    print(name + '\n')

    model = cp_model.CpModel()

    # Tighter UB on score
    if ub_colors == None:
        ub_colors = 1 + max([len(neighborhoods[i]) for i in range(nr_vertices)])

    if lb_score == None:
        lb_score = min(weight)
    if ub_score == None:
        ub_score = sum(weight)

    # VARIABLES

    # color/vertex matching matrix
    x_match = [[model.NewIntVar(0, 1, 'vertices%i color%f' % (i, j)) for j in range(ub_colors)] for i in range(nr_vertices)]

    # the color of each vertex
    x_color = [model.NewIntVar(lb_colors, ub_colors - 1, 'sommet%i' % i) for i in range(nr_vertices)]

    # the weight of each color
    x_weight = [model.NewIntVar(0, max(weight), 'color%i' % i) for i in range(ub_colors)]

    # the score of the solution
    x_score = model.NewIntVar(lb_score, ub_score, 'score')


    # CORE CONSTRAINTS

    # 1 color per vertex
    for i in range(nr_vertices):
        model.Add((sum(x_match[i][j] for j in range(ub_colors))) == 1)

    # the color of each vertex
    for i in range(nr_vertices):
        model.AddElement(x_color[i], [x_match[i][j] for j in range(ub_colors)], 1)
        # alternative 0/1 formulation
        # for j in range(ub_colors):
            # b = model.NewBoolVar("")
            # model.Add(x_match[i][j] == 1).OnlyEnforceIf(b)
            # model.Add(x_match[i][j] == 0).OnlyEnforceIf(b.Not())
            # model.Add(x_color[i] == j).OnlyEnforceIf(b)
            # model.Add(x_color[i] != j).OnlyEnforceIf(b.Not())

    # different colors between neighbours
    for i1 in range(nr_vertices):
        for i2 in neighborhoods[i1]:
            model.Add(x_color[i1] != x_color[i2])
            # alternative 0/1 formulation
            # for j in range(ub_colors):
                # model.Add(x_match[i1][j] + x_match[i2][j] <= 1)

    # the weight of each color
    for j in range(ub_colors):
        model.AddMaxEquality(x_weight[j], (x_match[i][j] * weight[i] for i in range(nr_vertices)))

    # the score of the solution
    model.Add(x_score == sum(x_weight))


    # SYMMETRY BREAKING CONSTRAINTS

    # (R0) sort colors in descending order of dominant vertices
    # - if the color is used, the dominant vertex is the vertex with smallest id amongst heaviest vertices
    # - if the color is not used, the dominant vertex is the virtual vertex with id=nr_vertices+j where j is the color id 
    x_dominant = [model.NewIntVar(0, j+nr_vertices, 'dominant%i' % j) for j in range(ub_colors)]
    for j in range(ub_colors):
        wvcp_globals.arg_max_no_zeros(model, j, x_dominant[j], [x_match[i][j] for i in range(nr_vertices)])
    cp_sat_utils.increasing_strict(model, x_dominant)
    # redundant (entailed) ordering constraint
    # cp_sat_utils.decreasing(model, x_weight)

    # (SR1)

    # (DR1)

    # (SR2) color each vertex with one of the first d+1 colors where d is the vertex's degree
    for i in range(nr_vertices):
        model.Add(x_color[i] <= len(neighborhoods[i]))

    # DR2
    for i in range(nr_vertices):
        z = [model.NewIntVar(0, len(neighborhoods[i]), '%i' % j) for j in range(len(neighborhoods[i])+1)]
        cp_sat_utils.global_cardinality(
            model,
            [x_color[u] for u in neighborhoods[i]],
            [j for j in range(len(neighborhoods[i])+1)],
            z
        )
        wvcp_globals.arg_min(model, x_color[i], z)

    model.AddDecisionStrategy(x_color, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_LOWER_HALF)
    model.Minimize(x_score)

    solver = cp_model.CpSolver()
    solution_printer = wvcp_primal_solutionPrinter.SolutionPrinter(nr_vertices, nr_edges, neighborhoods, x_match, x_color, x_weight, x_dominant, x_score, ub_colors)
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 4
    solver.parameters = sat_parameters_pb2.SatParameters(num_search_workers=4)
    solver.Solve(model, solution_printer)
    count, score = solution_printer.solution_count()
    time = solver.WallTime()
    print(time)

    return count, score, time
