'''
This will solve any sudoku :P
'''
def sudoku_solver(X):
    sudoku = [i[:] for i in X]
    def possible(d, i, j):
        if d in sudoku[i] or d in [sudoku[a][j] for a in range(9)]:
            return False
        a, b = i//3, j//3
        for y in range(a*3, (a+1)*3):
            for x in range(b*3, (b+1)*3):
                if sudoku[y][x] == d:
                    return False
        return True

    def get_peers(i,j):
        Q =  [(i, a) for a in range(9)]
        Q += [(a, j) for a in range(9)]
        a, b = i//3, j//3
        Q += [(y, x) for y in range(a*3, (a+1)*3) for x in range(b*3, (b+1)*3)]
        return set(Q)

    def check_validity():
        Q = len(sudoku) == 9 and all(len(i) == 9 for i in sudoku)
        if not Q:
            return False
        for i in range(9):
            for j in range(9):
                if type(sudoku[i][j]) == int and 0 <= sudoku[i][j] <= 9:
                    P = [sudoku[y][x] for y, x in get_peers(i, j) if sudoku[y][x] != 0 and (y, x) != (i, j)]
                    if sudoku[i][j] and sudoku[i][j] in P:
                        return False
                else:
                    return False
        return True
    
    if not check_validity():
        raise ValueError("LOL")
    
    repo = {(i, j): [a for a in range(1,10) if possible(a, i, j)] for i in range(0,9) for j in range(0, 9) if sudoku[i][j] == 0}
    K = sorted(repo.items(), key=lambda x: len(x[1]))

    def dfs(curr, visited):
        if len(visited) >= len(K):
            return sudoku
        i, j = curr
        for d in repo[(i, j)]:
            memo = []
            clone = repo[(i, j)][:]
            repo[(i, j)] = []
            for y, x in get_peers(i, j):
                if (y, x) in repo and d in repo[(y, x)] and (y, x) not in visited:
                    if len(repo[(y, x)]) == 1 and (y, x) != (i, j):
                        for y_, x_ in memo:
                            repo[(y_, x_)].append(d)
                        repo[(i, j)] = clone
                        return False
                    repo[(y, x)].remove(d)
                    memo.append((y, x))
            sudoku[i][j] = d

            nvis = visited | {(i, j)}
            if len(nvis) == len(repo):
                return sudoku
            Next = min([a for a in repo if a not in nvis], key=lambda x: len(repo[x]))

            pot = dfs(Next, nvis)

            if pot:
                return pot
            else:
                sudoku[i][j] = 0
                repo[(i, j)] = clone
                for y, x in memo:
                    repo[(y, x)].append(d)

        return False
    A = dfs(min(repo.keys(), key=lambda x:len(repo[x])) , set())
    if not A:
        raise ValueError("Error")
    return A
def sudoku_solver(sudoku):
    def possible(d, i, j):
        if d in sudoku[i] or d in [sudoku[a][j] for a in range(9)]:
            return False
        a, b = i//3, j//3
        for y in range(a*3, (a+1)*3):
            for x in range(b*3, (b+1)*3):
                if sudoku[y][x] == d:
                    return False
        return True

    def get_peers(i,j):
        Q =  [(i, a) for a in range(9)]
        Q += [(a, j) for a in range(9)]
        a, b = i//3, j//3
        Q += [(y, x) for y in range(a*3, (a+1)*3) for x in range(b*3, (b+1)*3)]
        return set(Q)

    SOLUTIONS_FOUNDS = []
    def check_validity():
        Q = len(sudoku) == 9 and all(len(i) == 9 for i in sudoku)
        if not Q:
            return False
        for i in range(9):
            for j in range(9):
                if type(sudoku[i][j]) == int and 0 <= sudoku[i][j] <= 9:
                    P = [sudoku[y][x] for y, x in get_peers(i, j) if sudoku[y][x] != 0 and (y, x) != (i, j)]
                    if sudoku[i][j] and sudoku[i][j] in P:
                        print(sudoku[i][j], P)
                        return False
                else:
                    return False
        return True
    
    if not check_validity():
        raise ValueError("LOL")
    
    repo = {(i, j): [a for a in range(1,10) if possible(a, i, j)] for i in range(0,9) for j in range(0, 9) if sudoku[i][j] == 0}
    K = sorted(repo.items(), key=lambda x: len(x[1]))
    print(possible(8, 5, 0))

    def dfs(curr, visited):
        if len(visited) >= len(K):
            return sudoku
        i, j = curr
        for d in repo[(i, j)]:
            memo = []
            clone = repo[(i, j)][:]
            repo[(i, j)] = []
            for y, x in get_peers(i, j):
                if (y, x) in repo and d in repo[(y, x)] and (y, x) not in visited:
                    if len(repo[(y, x)]) == 1 and (y, x) != (i, j):
                        for y_, x_ in memo:
                            repo[(y_, x_)].append(d)
                        repo[(i, j)] = clone
                        return False
                    repo[(y, x)].remove(d)
                    memo.append((y, x))
            sudoku[i][j] = d

            nvis = visited | {(i, j)}
            if len(nvis) == len(repo):
                SOLUTIONS_FOUNDS.append([i[:] for i in sudoku])
                return False
            Next = min([a for a in repo if a not in nvis], key=lambda x: len(repo[x]))

            pot = dfs(Next, nvis)

            if pot:
                return pot
            else:
                sudoku[i][j] = 0
                repo[(i, j)] = clone
                for y, x in memo:
                    repo[(y, x)].append(d)

        return False
    A = dfs(min(repo.keys(), key=lambda x:len(repo[x])) , set())
    if len(SOLUTIONS_FOUNDS) != 1:
        raise ValueError("Error")
    return SOLUTIONS_FOUNDS[0]
