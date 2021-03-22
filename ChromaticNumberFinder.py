'''
Accepts a map as string seperated by new lines, and determines the minimum number of colors required
to properly color the graph
'''
from collections import defaultdict
def helper(adj, colors):
    K = [*adj.keys()]
    def recurse(ind, assignments):
        if ind == len(adj):
            return True
        for c in colors[K[ind]]:
            print(c, assignments, adj[K[ind]])
            if c not in (assignments[i] for i in adj[K[ind]] if i in assignments):
                A = recurse(ind + 1, {**assignments, K[ind]: c})
                if A:
                    return A
        return None
    return recurse(0, dict())

def color(M):
    M = M.strip('\n').split('\n')
    seen, H, W = set(), len(M), len(M[0])
    neighbours = defaultdict(set)
    for i in range(H):
        for j in range(W):
            current = (i, j)
            if current not in seen:
                stack = [current]
                while stack:
                    y, x = stack.pop()
                    for y_, x_ in (y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x):
                        if min(y_, x_) > -1 and y_ < H and x_ < W and (y_, x_) not in seen:
                            if M[y_][x_] == M[i][j]:
                                stack.append((y_, x_))
                            else:
                                neighbours[M[i][j]].add(M[y_][x_])
                                neighbours[M[y_][x_]].add(M[i][j])
                    seen.add((y, x))
    neighbours = {i: set(j) for i, j in neighbours.items()}
    X = 'RGB'
    for i in range(1, 4):
        colors = {j: {*X[:i]} for j in neighbours}
        if helper(neighbours, colors):
            return i
    return 4
