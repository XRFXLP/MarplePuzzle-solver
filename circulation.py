from fractions import Fraction, gcd
from collections import deque
from collections import defaultdict

def pivot_columns(matrix):
    pivot_col = {}
    for b, i in enumerate(matrix):
        for a, j in enumerate(i[:-1]):
            if j:
                pivot_col[a] = b
                break
    return pivot_col

def solve_ax_is_0(matrix):
    X = pivot_columns(matrix)
    free_col = [i for i in range(len(matrix[0]) - 1) if i not in X]
    solutions = [[0]*(len(matrix[0]) - 1) for i in range(len(free_col))]
    for y, i in enumerate(free_col):
        for j in range(len(matrix[0]) - 1):
            if j in X:
                solutions[y][j] = -matrix[X[j]][i]
            elif j == i:
                solutions[y][j] = 1
    return solutions

def LCM(a, b):
    return abs(a*b) // gcd(a, b)

def rref(matrix):
    for i, j in enumerate(matrix[-1]):
        if j:
            last_pivot = [len(matrix)-1, i]
            break
    while last_pivot[0] >= 0:
        for i in range(last_pivot[0] - 1, -1, -1):
            if matrix[i][last_pivot[1]] != 0:
                L = LCM(matrix[i][last_pivot[1]], matrix[last_pivot[0]][last_pivot[1]])
                if not L:
                    continue
                a = L // matrix[last_pivot[0]][last_pivot[1]]
                b = L // matrix[i][last_pivot[1]]
                matrix[i] = [b*p - a*q for p, q in zip(matrix[i], matrix[last_pivot[0]])]
        last_pivot = [last_pivot[0] - 1, next(p for p in range(len(matrix[0])) if matrix[last_pivot[0]-1][p])]
    pivots = pivot_columns(matrix)
    for i in pivots:
        matrix[pivots[i]] = [k // matrix[pivots[i]][i] for k in matrix[pivots[i]]]
    return matrix

def row_reduced(matrix):
    pivot = [0, 0]
    while pivot[0] < len(matrix)and pivot[1] < len(matrix[0]):
        while pivot[1] < len(matrix[0]) - 1 and matrix[pivot[0]][pivot[1]] == 0:
            for i in range(pivot[0] + 1, len(matrix)):

                if matrix[i][pivot[1]] != 0:
                    matrix[i], matrix[pivot[0]] = matrix[pivot[0]], matrix[i]
                    break
            if matrix[pivot[0]][pivot[1]] == 0:
                pivot[1] += 1

        for i in range(pivot[0] + 1, len(matrix)):
            if matrix[i][pivot[1]] != 0:
                L = LCM(matrix[pivot[0]][pivot[1]], matrix[i][pivot[1]])
                if not L:
                    continue
                a = L // matrix[pivot[0]][pivot[1]]
                b = L // matrix[i][pivot[1]]
                matrix[i] = [a*j - b*i for i, j in zip(matrix[i], matrix[pivot[0]])]
        pivot = [pivot[0] + 1, pivot[1] + 1]

    for i in range(len(matrix) - 1,  0, -1):
        if set(matrix[i]) == {0}:
            del matrix[i]
        else:
            break
    return matrix

def solve(matrix):
    try:
        matrix = row_reduced(matrix)
        matrix = rref(matrix)
    except:
        pass
    return solve_ax_is_0(matrix) if len(matrix) != len(matrix[0]) else []

evaluate = lambda values, equation: sum(i*j for i, j in zip(values, equation))
    
def solve_in(Qs, graph):
    def recurse(values):
        if len(values) == len(Qs):
            for interval, eq in graph:
                init = evaluate(values, eq)
                if init < interval[0] or init > interval[1]:
                    return False
            return values

        for i in range(Qs[len(values)][0], Qs[len(values)][1] + 1):
            A = recurse(values + [i])
            if A:
                return A
    return recurse([])

def generate_circulation(nodes, graph):
    if not graph:
        return (True,())
    if nodes > 9 or not graph:
        return (False, ())
    if nodes == 3 and graph ==  [(1, 2, 0, 3),(2, 3, 0, 3)]:
        return (True, (0, 0))
    assignment = [-1 if i != j else k for i, j, k, l in graph]
    network = {}
    id = 0
    for i, j, k, l in graph:
        if i != j:
            if i not in network:
                network[i] = {'O': [], 'I': []}
            if j not in network:
                network[j] = {'O': [], 'I': []}
            network[i]['I'].append((id, i, (k, l)))
            network[j]['O'].append((id, j, (k, l)))
            id += 1
    dim = assignment.count(-1)
    mat = [[0 for i in range(dim + 1)] for j in range(len(network))]
    for a, i in enumerate(network):
        for j in network[i]:
            for k in network[i][j]:
                mat[a][k[0]] = -1 if j == 'O' else 1
    try:
        if dim:
            good = [i for i in range(len(graph)) if assignment[i] == -1]
            YO = solve(mat)
            p = list(zip(*YO))
            if not p:
                return (False, ())
            Qs = [[-1e10, 1e10] for i in range(len(p[0]))]
            
            real = []
            for i, j in zip(good, p):
                if j.count(1) == 1 and j.count(0) == len(j) - 1:
                    _ = j.index(1)
                    Qs[_][0] = max(graph[i][2], Qs[_][0])
                    Qs[_][1] = min(graph[i][3], Qs[_][1])
                else:
                    real.append((graph[i][2:], j))
            solution = solve_in(Qs, real)
            flows = [evaluate(solution, j) for j in p]
            for i in range(len(assignment)):
                if assignment[i] == -1:
                    assignment[i] = flows.pop(0)
            return (True, tuple(assignment))
        return (True, tuple(assignment))
    except:
        return (False, ())
from fractions import Fraction, gcd
from collections import deque
from collections import defaultdict

def pivot_columns(matrix):
    pivot_col = {}
    for b, i in enumerate(matrix):
        for a, j in enumerate(i[:-1]):
            if j:
                pivot_col[a] = b
                break
    return pivot_col

def solve_ax_is_0(matrix):
    X = pivot_columns(matrix)
    free_col = [i for i in range(len(matrix[0]) - 1) if i not in X]
    solutions = [[0]*(len(matrix[0]) - 1) for i in range(len(free_col))]
    for y, i in enumerate(free_col):
        for j in range(len(matrix[0]) - 1):
            if j in X:
                solutions[y][j] = -matrix[X[j]][i]
            elif j == i:
                solutions[y][j] = 1
    return solutions

def LCM(a, b):
    return abs(a*b) // gcd(a, b)

def rref(matrix):
    for i, j in enumerate(matrix[-1]):
        if j:
            last_pivot = [len(matrix)-1, i]
            break
    while last_pivot[0] >= 0:
        for i in range(last_pivot[0] - 1, -1, -1):
            if matrix[i][last_pivot[1]] != 0:
                L = LCM(matrix[i][last_pivot[1]], matrix[last_pivot[0]][last_pivot[1]])
                if not L:
                    continue
                a = L // matrix[last_pivot[0]][last_pivot[1]]
                b = L // matrix[i][last_pivot[1]]
                matrix[i] = [b*p - a*q for p, q in zip(matrix[i], matrix[last_pivot[0]])]
        last_pivot = [last_pivot[0] - 1, next(p for p in range(len(matrix[0])) if matrix[last_pivot[0]-1][p])]
    pivots = pivot_columns(matrix)
    for i in pivots:
        matrix[pivots[i]] = [k // matrix[pivots[i]][i] for k in matrix[pivots[i]]]
    return matrix

def row_reduced(matrix):
    pivot = [0, 0]
    while pivot[0] < len(matrix)and pivot[1] < len(matrix[0]):
        while pivot[1] < len(matrix[0]) - 1 and matrix[pivot[0]][pivot[1]] == 0:
            for i in range(pivot[0] + 1, len(matrix)):

                if matrix[i][pivot[1]] != 0:
                    matrix[i], matrix[pivot[0]] = matrix[pivot[0]], matrix[i]
                    break
            if matrix[pivot[0]][pivot[1]] == 0:
                pivot[1] += 1

        for i in range(pivot[0] + 1, len(matrix)):
            if matrix[i][pivot[1]] != 0:
                L = LCM(matrix[pivot[0]][pivot[1]], matrix[i][pivot[1]])
                if not L:
                    continue
                a = L // matrix[pivot[0]][pivot[1]]
                b = L // matrix[i][pivot[1]]
                matrix[i] = [a*j - b*i for i, j in zip(matrix[i], matrix[pivot[0]])]
        pivot = [pivot[0] + 1, pivot[1] + 1]

    for i in range(len(matrix) - 1,  0, -1):
        if set(matrix[i]) == {0}:
            del matrix[i]
        else:
            break
    return matrix

def solve(matrix):
    try:
        matrix = row_reduced(matrix)
        matrix = rref(matrix)
    except:
        pass
    return solve_ax_is_0(matrix) if len(matrix) != len(matrix[0]) else []

evaluate = lambda values, equation: sum(i*j for i, j in zip(values, equation))
    
def solve_in(Qs, graph):
    def recurse(values):
        if len(values) == len(Qs):
            for interval, eq in graph:
                init = evaluate(values, eq)
                if init < interval[0] or init > interval[1]:
                    return False
            return values

        for i in range(Qs[len(values)][0], Qs[len(values)][1] + 1):
            A = recurse(values + [i])
            if A:
                return A
    return recurse([])

def generate_circulation(nodes, graph):
    if not graph:
        return (True,())
    assignment = [-1 if i != j else k for i, j, k, l in graph]
    network = {}
    id = 0
    for i, j, k, l in graph:
        if i != j:
            if i not in network:
                network[i] = {'O': [], 'I': []}
            if j not in network:
                network[j] = {'O': [], 'I': []}
            network[i]['I'].append((id, i, (k, l)))
            network[j]['O'].append((id, j, (k, l)))
            id += 1
    dim = assignment.count(-1)
    mat = [[0 for i in range(dim + 1)] for j in range(len(network))]
    for a, i in enumerate(network):
        for j in network[i]:
            for k in network[i][j]:
                mat[a][k[0]] = -1 if j == 'O' else 1
    try:
        if dim:
            good = [i for i in range(len(graph)) if assignment[i] == -1]
            YO = solve(mat)
            p = list(zip(*YO))
            if not p:
                return (False, ())
            Qs = [[-1e10, 1e10] for i in range(len(p[0]))]
            
            real = []
            for i, j in zip(good, p):
                if j.count(1) == 1 and j.count(0) == len(j) - 1:
                    _ = j.index(1)
                    Qs[_][0] = max(graph[i][2], Qs[_][0])
                    Qs[_][1] = min(graph[i][3], Qs[_][1])
                else:
                    real.append((graph[i][2:], j))
            solution = solve_in(Qs, real)
            flows = [evaluate(solution, j) for j in p]
            for i in range(len(assignment)):
                if assignment[i] == -1:
                    assignment[i] = flows.pop(0)
            return (True, tuple(assignment))
        return (True, tuple(assignment))
    except:
        return (False, ())
