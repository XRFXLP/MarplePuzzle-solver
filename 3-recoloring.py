def helper(adj, colors):
    colors = {i: set(['R', 'G', 'B']) - set([j]) for i, j in colors.items()}
    K = [*adj.keys()]
    indexM = {K[i]: i  for i in range(len(K))}
    colori = [(i, tuple(colors[K[i]])) for i in range(len(K))]

    def recurse(ind, assignments, possibilities):
        if ind == len(adj):
            return assignments
        for c in colors[K[ind]]:
            removed = []
            if c not in (assignments[i] for i in adj[K[ind]] if i in assignments):
                clone = [(i, tuple(filter(lambda x: x != c, j))) if K[i] in adj[K[ind]] else (i, j)  for i, j in possibilities if j and K[i] not in assignments and i != ind]
                if not clone:
                    return {**assignments, K[ind]: c}
                N = min(clone, key = lambda x: len(x[1]))
                if not N[1]:
                    break
                A = recurse(N[0], {**assignments, K[ind]: c}, clone)
                if A:
                    return A
        return None
    return recurse(0, dict(), colori)

def connected_components(Adj):
    visited, cp = set(), []
    for i in Adj:
        if i not in visited:
            stack = [i]
            t = set()
            while stack:
                c = stack.pop()
                t.add(c)
                stack += [n for n in Adj[c] if n not in visited]
                visited.add(c)
            cp.append(t)
    return cp
def assign_new_colors(adj, colors):
    cp = connected_components(adj)
    A = {}
    for c in cp:
        cl = {i: colors[i] for i in c}
        aj = {i: adj[i] for i in c}
        X = helper(aj, cl)
        if X == None:
            return None
        else:
            A.update(X)
    return None if len(A) != len(adj) else A
def helper(adj, colors):
    colors = {i: set(['R', 'G', 'B']) - set([j]) for i, j in colors.items()}
    K = [*adj.keys()]
    colori = [(i, tuple(colors[K[i]])) for i in range(len(K))]
    def recurse(ind, assignments, possibilities):
        for c in colors[K[ind]]:
            if c not in (assignments[i] for i in adj[K[ind]] if i in assignments):
                clone = [(i, tuple(filter(lambda x: x != c, j))) if K[i] in adj[K[ind]] else (i, j)  for i, j in possibilities if j and K[i] not in assignments and i != ind]
                if not clone:                    return {**assignments, K[ind]: c}
                N = min(clone, key = lambda x: len(x[1]))
                if not N[1]:                    break
                A = recurse(N[0], {**assignments, K[ind]: c}, clone)
                if A:                           return A
        return None
    return recurse(0, dict(), colori)

def connected_components(Adj):
    visited, cp = set(), []
    for i in Adj:
        if i not in visited:
            stack, t = [i], set()
            while stack:
                c = stack.pop()
                t.add(c)
                stack += [n for n in Adj[c] if n not in visited]
                visited.add(c)
            cp.append(t)
    return cp
def assign_new_colors(adj, colors):
    cp, A  = connected_components(adj), {}
    for c in cp:
        cl = {i: colors[i] for i in c}
        aj = {i: adj[i] for i in c}
        X = helper(aj, cl)
        if X == None:            return None
        else:                    A.update(X)
    return None if len(A) != len(adj) else A
