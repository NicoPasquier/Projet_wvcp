from ortools.sat.python import cp_model
from ortools.sat import sat_parameters_pb2

from . import cp_sat_utils
from . import wvcp_globals
from . import wvcp_joint_solutionPrinter


def joint(thread, rule, time_limit, name, nr_vertices, nr_edges, neighborhoods, arc, weight, lb_colors=0, ub_colors=None, lb_score=None, ub_score=None):
    print(name + '\n')

    model = cp_model.CpModel()

    # Tighter UB on score
    if ub_colors == None:
        ub_colors = 1 + max([len(neighborhoods[i]) for i in range(nr_vertices)])

    if lb_score == None:
        lb_score = max(weight)
    if ub_score == None:
        ub_score = sum(weight)

    # VARIABLES OF PRIMAL
    # color/vertex matching matrix
    x_match = [[model.NewIntVar(0, 1, 'vertices%i color%f' % (i, j)) for j in range(ub_colors)] for i in
               range(nr_vertices)]
    # the color of each vertex
    x_color = [model.NewIntVar(lb_colors, ub_colors - 1, 'sommet%i' % i) for i in range(nr_vertices)]
    # the weight of each color
    x_weight = [model.NewIntVar(0, max(weight), 'color%i' % i) for i in range(ub_colors)]
    # the score of the solution
    x_score = model.NewIntVar(lb_score, ub_score, 'score')

    # VARIABLES OF DUAL
    x = [model.NewIntVar(0, 1, "x%i%f" % (i[0], i[1])) for i in arc]
    y_weight = [model.NewIntVar(0, max(weight), "weight%i" % i) for i in range(len(arc))]
    y = model.NewIntVar(0, sum(weight), 'y')
    # the score of the solution
    y_score = model.NewIntVar(lb_score, ub_score, 'score')

    y_dominated = [model.NewIntVar(0, 1, 'y_dominated%i' % i) for i in range(nr_vertices)]

    # CORE CONSTRAINTS OF PRIMAL

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
    x_dominant = [model.NewIntVar(0, j + nr_vertices, 'dominant%i' % j) for j in range(ub_colors)]
    for j in range(ub_colors):
        wvcp_globals.arg_max_no_zeros(model, j, x_dominant[j], [x_match[i][j] for i in range(nr_vertices)])
    cp_sat_utils.increasing_strict(model, x_dominant)
    # redundant (entailed) ordering constraint
    # cp_sat_utils.decreasing(model, x_weight)

    # (SR1)

    # (DR1)

    # (SR2) color each vertex with one of the first d+1 colors where d is the vertex's degree
    if "SR2" in rule:
        for i in range(nr_vertices):
            model.Add(x_color[i] <= len(neighborhoods[i]))

    # DR2
    if "DR2" in rule:
        for i in range(nr_vertices):
            z = [model.NewIntVar(0, len(neighborhoods[i]), '%i' % j) for j in range(len(neighborhoods[i]) + 1)]
            cp_sat_utils.global_cardinality(
                model,
                [x_color[u] for u in neighborhoods[i]],
                [j for j in range(len(neighborhoods[i]) + 1)],
                z
            )
            wvcp_globals.arg_min(model, x_color[i], z)

    # CORE CONSTRAINTS OF DUAL
    for i in range(len(arc)):
        for j in range(i + 1, len(arc)):
            if arc[i][0] == arc[j][0] and not ((arc[i][1], arc[j][1]) in arc) and not (
                    (arc[j][1], arc[i][1]) in arc):
                model.Add(x[i] + x[j] <= 1)
            if arc[i][0] == arc[j][1] or arc[i][1] == arc[j][0]:
                model.Add(x[i] + x[j] <= 1)
            if arc[i][1] == arc[j][1]:
                model.Add(x[i] + x[j] <= 1)

    for i in range(len(arc)):
        model.Add(y_weight[i] == x[i] * weight[arc[i][1]])

    model.Add(y == sum(y_weight))

    # the score of the solution
    model.Add(y_score == sum(weight) - y)

    # PRIMAL/DUAL CHANNELING CONSTRAINTS
    cp_sat_utils.global_cardinality(
        model,
        x_dominant,
        [i for i in range(nr_vertices)],
        [1-y_dominated[i] for i in range(nr_vertices)]
    )

    for i in range(len(arc)):
        b = model.NewBoolVar("")
        model.Add(x[i] == 1).OnlyEnforceIf(b)
        model.Add(x_color[arc[i][0]] == x_color[arc[i][1]]).OnlyEnforceIf(b)
        """model.Add(x[i] == 0).OnlyEnforceIf(b.Not())
        model.Add(x_color[arc[i][0]] == x_color[arc[i][1]]).OnlyEnforceIf(b.Not())
        model.Add(x_color[arc[i][0]] != x_color[arc[i][1]]).OnlyEnforceIf(b.Not())"""

    # objectives
    model.Add(x_score == y_score)

    # JOINT-DUAL CONSTRAINTS
    ins = [[] for i in range(nr_vertices)]
    outs = [[] for i in range(nr_vertices)]
    for a in range(len(arc)):
        ins[arc[a][1]].append(a)
        outs[arc[a][0]].append(a)

    for i in range(nr_vertices):
        # disconnected vertices are dominant
        if ins[i] == [] and outs[i] == []:
            model.Add(y_dominated[i] == 0)
        # backward vertices are dominant (this constraint may be merged with above constraint)
        if ins[i] == [] and outs[i] != []:
            model.Add(y_dominated[i] == 0)
        # forward vertices are dominated iff backward dominated
        if ins[i] != [] and outs[i] == []:
            model.Add(y_dominated[i] == sum(x[hi] for hi in ins[i]))
        # backward and forward vertices
        if ins[i] != [] and outs[i] != []:
            k = model.NewIntVar(0, 1, "k")
            model.AddMaxEquality(k, [x[ij] for ij in outs[i]])
            model.Add(1 - y_dominated[i] >= k)
            # model.Add(1 - y_dominated[i] >= max(x[ij] for ij in outs[i]))
            model.Add(y_dominated[i] >= sum(x[hi] for hi in ins[i]))
        # backward and forward vertices are assumed dominant if not grouped
        # if ins[i] != [] and outs[i] == []:
            # model.Add(1-y_dominated[i] >= (1-max(x[ij] for ij in outs[i]))*(1-sum(x[hi] for hi in ins[i])))

    model.Minimize(x_score)

    solver = cp_model.CpSolver()
    solution_printer = wvcp_joint_solutionPrinter.SolutionPrinter(nr_vertices, nr_edges, neighborhoods, x_match, x_color, x_weight, x_dominant, x_score, ub_colors)
    solver.parameters.enumerate_all_solutions = True
    solver.parameters = sat_parameters_pb2.SatParameters(max_time_in_seconds=time_limit, num_search_workers=thread)
    status = solver.Solve(model, solution_printer)
    count, score = solution_printer.solution_count()
    time = solver.WallTime()
    optimal = False
    if status == cp_model.OPTIMAL:
        optimal = True
    print(time)

    return score, optimal, time
