'''
A simple program to solve 7 by 7 skyscraper puzzle
'''

from functools import lru_cache

def check(vector, start, final):
    sc, Ms = 1, vector[0]
    fc, Mf = 1, vector[6]
    for i in range(1, 7):
        if vector[i] > Ms:
            sc += 1
            Ms = vector[i]
        if vector[6 - i] > Mf:
            fc += 1
            Mf = vector[6 - i]
    if start and sc != start:        return False
    if final and fc != final:        return False
    return True
    
def not_in_row_or_col(board, y, x):
    Q = board[y][x]
    R = sum([board[y][a] for a in range(7)], [])
    C = sum([board[a][x] for a in range(7)], [])
    for i in Q:
        if R.count(i) == 1 or C.count(i) == 1:
            return i
    return 0

@lru_cache(maxsize=None)
def get_peers(i, j):
    Q = [(i, a) for a in range(7)]
    Q +=[(a, j) for a in range(7) if a != i]
    return Q

def remove_from_row_and_col(board, y, x):
    for b in range(7):
        if b != x and board[y][x][0] in board[y][b]:
            board[y][b].remove(board[y][x][0])
        if b != y and board[y][x][0] in board[b][x]:
            board[b][x].remove(board[y][x][0])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def get_starting_coordinates_direction(i):
    return (0, i, (1, 0)) if i < 7 else (i % 7, 6, (0, -1)) if i < 14 else (6, 6 - (i % 7), (-1, 0)) if i < 21 else (6 -  (i % 7), 0, (0, 1))

def get_line(board, start, end):
    if max(start + end) > 6 or min(start + end) < 0:
        return []
    diff = sub(end, start)
    d = (0 if diff[0] == 0 else diff[0]//abs(diff[0]), 0 if diff[1] == 0 else diff[1]//abs(diff[1]))
    y, x = start
    coll = []
    while True:
        if len(board[y][x]) == 1:
            coll += board[y][x]

        if (y, x) == end:
            return coll
        y, x = (y + d[0], x + d[1])
        
def solve_puzzle(clues):
    board = [[list(range(1,8)) for i in range(7)] for j in range(7)]
    count = 0
    while count < 4:
        count += 1
        for i, j in enumerate(clues):
            y, x, d = get_starting_coordinates_direction(i)
            y_, x_ = y, x
            curr = 1
            if j == 1:
                board[y][x] = [7]
            while curr <=7:
                board[y][x] = [a for a in board[y][x] if j - (8 - a) < curr]
                if len(board[y][x]) == 1:
                    a = board[y][x][0]
                    if j - ( 8 -  a) == curr - 1 and (y, x) != (y_, x_):
                        by, bx = sub((y, x), d)
                        while True:
                            to_remove = []  
                            front = board[by + d[0]][bx + d[1]] if (by, bx) != (y  -  d[0], x  - d[1]) else []
                            back  = board[by - d[0]][bx - d[1]] if min(by-d[0], bx - d[1]) > -1  and max(by-d[0], bx - d[1]) < 7 else []
                            for pot in board[by][bx]:
                                if front and not any(op > pot for op in front):
                                    to_remove.append(pot)
                                elif back and not any(op < pot for op in back):
                                    to_remove.append(pot)
                            
                            for g in to_remove:
                                board[by][bx].remove(g)
                            
                            if (by, bx) == (y_, x_):
                                break
                            by, bx = sub((by, bx), d)
                for v in board[y][x]:
                    if j - (8 - v) == curr - 1 and (y, x) != (y_, x_):
                        back = get_line(board, sub((y, x), d), (y_, x_))
                        if sorted(back, reverse=True) != back:
                            board[y][x].remove(v)
                            break               
                k = not_in_row_or_col(board, y, x)
                if k:
                    board[y][x] = [k]
                if len(board[y][x]) == 1:
                    remove_from_row_and_col(board, y, x)
                y, x = (y + d[0], x + d[1])
                curr += 1
    possible = {(i, j): sorted(board[i][j]) for i in range(7) for j in range(7)}
    LT = {i:len(possible[i]) for i in possible}
    grid  = [[0 if LT[(j, i)] > 1 else possible[(j, i)][0]for i in range(7)] for j in range(7)]

    def dfs(y, x):
        for d in possible[(y, x)]:
            memo = []
            to_continue = False
            for y_, x_ in get_peers(y, x):
                if d in possible[(y_, x_)]:
                    if not(y_ == y and x_ == x) and LT[(y_, x_)] < 2 and grid[y_][x_] == 0:
                        for dy, dx in memo:
                            possible[(dy, dx)].append(d)
                            LT[(dy, dx)] += 1
                            possible[(dy, dx)].sort()
                        to_continue = True
                        break
                    possible[(y_, x_)].remove(d)
                    LT[(y_, x_)] -= 1
                    memo.append((y_, x_))

            if to_continue:
                continue

            grid[y][x] = d
            if 0 not in grid[y]:
                left_clue  = clues[-1 - y]
                right_clue = clues[ 7 + y]
                if not check(grid[y], left_clue, right_clue):
                    grid[y][x] = 0
                    for y_, x_ in memo:
                        possible[(y_, x_)].append(d)
                        LT[(y_, x_)] += 1
                        possible[(y_, x_)].sort()
                    continue
            col = [grid[0][x], grid[1][x], grid[2][x], grid[3][x],grid[4][x],grid[5][x],grid[6][x]]       
            if 0 not in col:
                left_clue = clues[x]
                right_clue = clues[20 - x]
                if not check(col, left_clue, right_clue):
                    grid[y][x] = 0
                    for y_, x_ in memo:
                        possible[(y_, x_)].append(d)
                        LT[(y_, x_)] += 1
                        possible[(y_, x_)].sort()
                    continue

            try:
                y__, x__ = min([u for u in possible if not grid[u[0]][u[1]]], key=LT.__getitem__)
            except:
                return grid

            A = dfs(y__, x__)
            if A:
                return A
            else:
                grid[y][x] = 0
                for y_, x_ in memo:
                    possible[(y_, x_)].append(d)
                    LT[(y_, x_)] += 1
                    possible[(y_, x_)].sort()

    return dfs(*min([u for u in possible if not grid[u[0]][u[1]]], key=LT.__getitem__))
