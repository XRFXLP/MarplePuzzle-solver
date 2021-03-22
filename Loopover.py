'''
An efficient program to solve loopover
'''
from collections import deque
def SOLVED(scrambled, solved, INVERSE):
    scrambled = list(map(lambda x: list(map(lambda y:INVERSE[tuple(y)], x)), scrambled))
    return scrambled == solved
def parity(board):
    Q = [[1 if board[i][j]!=[i, j] else 0 for j in range(len(board[0]))] for i in range(len(board))]
    if sum(sum(i) for i in Q) != 2:
        return "Fucked up"
    if Q[-1][-1] == 1:
        if Q[-2][-1] == 1:
            return 'V'
        if Q[-1][-2] == 1:
            return 'H'
    return "O"
def loopover(scrambled, solved):
    print(scrambled, solved)
    MAP = {solved[i][j]:[i, j] for j in range(len(solved[0])) for i in range(len(solved))}
    INVERSE = {tuple(j): i for i, j in MAP.items()}
    scrambled = list(map(lambda x: list(map(lambda y:MAP[y], x)), scrambled))
    to_find = [0, 0]
    current = [0, 0]
    H, W = len(scrambled), len(scrambled[0])

    RS = []
    if SOLVED(scrambled, solved, INVERSE):
        return RS
    #Perform up/down movement in matrix
    #c is number of column in which the movement is required
    #n is number of moves required
    def ud(matrix, c, n):
        nonlocal RS
        if n < 0:
            RS += [f'{"U"}{c}']*abs(n)
        elif n > 0:
            RS += [f'{"D"}{c}']*abs(n)
        column = deque([i[c] for i in matrix])
        column.rotate(n)
        for i in range(len(matrix)):
            matrix[i][c] = column.popleft()
        return matrix

    #Performs left/right movement in matrix
    #r is the number of row in which the movement is required
    #n is number of moves required, which can be positive or negative
    def lr(matrix, r, n):
        nonlocal RS
        if n > 0:
            RS += [f'{"R"}{r}']*abs(n)
        elif n < 0:
            RS += [f'{"L"}{r}']*abs(n)
        row = deque(matrix[r])
        row.rotate(n)
        matrix[r] = list(row)
        return matrix

    def finder(to_find, mode = 'H'):
        for i in range(H):
            for j in range(W):
                if scrambled[i][j] == to_find:
                    if mode == 'H':
                        if W - 1 == to_find[1]:
                            to_find[0], to_find[1] = to_find[0] + 1, 0
                        else:
                            to_find[1] = to_find[1] + 1
                    else:
                        to_find[0] += 1
                    return [i, j]




    while to_find[1] < W - 1:
        location = finder(to_find)
        if location[0] == current[0]:
            location[0] += 1
            scrambled = ud(scrambled, location[1], 1)



        scrambled = lr(scrambled, location[0], current[1] - location[1])

        location[1] = current[1]
        scrambled = ud(scrambled, location[1], current[0] - location[0])

        current = to_find[::]

    to_find = [1, 0]
    current = [1, 0]


    while to_find[0] < H - 1:
        location = finder(to_find)
        if location[0] == current[0]:
            temp = W - 1 - location[1]
            scrambled = lr(scrambled, location[0], temp)
            location[1] = W - 1
            scrambled = ud(scrambled, W - 1, 1)
            location[0] += 1
            scrambled = lr(scrambled, current[0], -temp)

        if location[0] != current[0] + 1 and location[1] == W - 1:
            scrambled = ud(scrambled, location[1], current[0] + 1 - location[0])
            location[0] = current[0] + 1

        scrambled = lr(scrambled, location[0], current[1] - location[1])

        for each_row in range(current[0]):
            scrambled = lr(scrambled, each_row, current[1] - W + 1)
        scrambled = ud(scrambled, current[1], current[0] - location[0])
        for each_row in range(current[0]):
            scrambled = lr(scrambled, each_row, -(current[1] - W + 1))

        current = to_find[::]

    if SOLVED(scrambled, solved, INVERSE):
        return RS

    to_find = [0, W - 1]
    current = [0, W - 1]

    while to_find[0] < H - 1:
        location = finder(to_find, 'W')
        if location[0] == H - 1:
            scrambled = lr(scrambled, H - 1, W - 1 - location[1])
            location = [H - 1, W - 1]
        saved = -location[0] - 1
        scrambled = ud(scrambled, W - 1, saved)
        location = [H - 1, W - 1]
        scrambled = lr(scrambled, H - 1, -1)
        location = [H - 1, W - 2]
        scrambled = ud(scrambled, W - 1, -saved)
        scrambled = lr(scrambled, H - 1, 1)
        scrambled = ud(scrambled, W - 1,-1)

    scrambled = lr(scrambled, H - 1, -finder([H - 1, 0])[1])
    if SOLVED(scrambled, solved, INVERSE):
        return RS

    #Assuming that now the whole board except the last row is solved
    temp = [H - 1, 0]
    location = finder(temp)
    scrambled = lr(scrambled, H - 1, -location[1])
    scrambled = ud(scrambled, W - 1, 1)
    scrambled = lr(scrambled, H - 1, 1)
    scrambled = ud(scrambled, W - 1, -1)
    #^^ This is setup part for solving the last row(I think(but I can be wrong))
    K = [H - 1, 1]
    for i in range(W-2):
        K_D = K[::]
        location = finder(K)
        if location == [H - 2, W - 1]:
            last = [K_D[0], K_D[1] - 1]
            location_last = finder(last[::])
            scrambled = lr(scrambled, H - 1, W - 1 - location_last[1] - 1)
            scrambled = ud(scrambled, W - 1, 1)
            if K_D != [H - 1, W - 2]:
                scrambled = lr(scrambled, H - 1, - 1)
            else:
                scrambled = lr(scrambled, H - 1, W - 2 - finder(K_D)[1])
            scrambled = ud(scrambled, W - 1, -1)
        elif location[0] == H - 1:
            last = [K_D[0], K_D[1] - 1]
            scrambled = lr(scrambled, H - 1, W - 1 - location[1])
            scrambled = ud(scrambled, W - 1, 1)
            location_last = finder(last[::])
            scrambled = lr(scrambled, H - 1, W - 1 - location_last[1] - 1)
            scrambled = ud(scrambled, W - 1, -1)
            scrambled = lr(scrambled, H - 1, -1)
    
    scrambled = lr(scrambled, H - 1, -finder([H - 1, 0])[1])
    if SOLVED(scrambled, solved, INVERSE):
        return RS
    P = parity(scrambled)

    if P == 'V' and len(scrambled) % 2 == 1:
        scrambled = lr(scrambled, H - 1,  1)
        scrambled = ud(scrambled, W - 1,  1)
        scrambled = lr(scrambled, H - 1, -1)
        scrambled = ud(scrambled, W - 1, -1)
    P = parity(scrambled)
    if P == 'V':
        scrambled = lr(scrambled, H - 1, -1)
        scrambled = ud(scrambled, W - 1,  1)
        scrambled = lr(scrambled, H - 1,  1)
        scrambled = ud(scrambled, W - 1, -1)
        scrambled = lr(scrambled, H - 1, -1)
        scrambled = lr(scrambled, H - 1,  1)
        scrambled = ud(scrambled, W - 1, -1)
        to_find = [H - 1, W - 1]
        while 1:
            location = finder(to_find, 'W')
            if location[1] == W - 1:
                scrambled = ud(scrambled, W - 1, -location[0] - 1)
                scrambled = lr(scrambled, H - 1, -1)
                scrambled = ud(scrambled, W - 1, location[0] + 1)
                scrambled = lr(scrambled, H - 1, 1)
                scrambled = ud(scrambled, W - 1, -1)
            elif location[0] == H - 1:
                scrambled = lr(scrambled, H - 1, W - 1 -location[1])
                scrambled = ud(scrambled, W - 1, -1)
            if to_find[0] == H:
                to_find = [0, W - 1]
            if to_find[0] == H - 1:
                break
    elif P == 'H':
        scrambled = ud(scrambled, W - 1, -1)
        scrambled = lr(scrambled, H - 1,  1)
        scrambled = ud(scrambled, W - 1,  1)
        scrambled = lr(scrambled, H - 1, -1)
        scrambled = ud(scrambled, W - 1, -1)
        scrambled = ud(scrambled, W - 1,  1)
        scrambled = lr(scrambled, H - 1, -1)
        to_find = [H - 1, W - 1]
        while 1:
            print(to_find)
            location = finder(to_find)
            if location[0] == H - 1:
                scrambled = lr(scrambled, H - 1, -location[1] - 1)
                scrambled = ud(scrambled, W - 1, -1)
                scrambled = lr(scrambled, H - 1, location[1] + 1)
                scrambled = ud(scrambled, W - 1, 1)
                scrambled = lr(scrambled, H - 1, -1)
            elif location[1] == W - 1:
                scrambled = ud(scrambled, W - 1, H - 1 -location[0])
                scrambled = lr(scrambled, H - 1, -1)
            if to_find[0] == H:
                to_find = [H - 1, 0]
            if to_find[1] == W - 1:
                break

        for i in scrambled:
            print(i)

    if SOLVED(scrambled, solved, INVERSE):
        return RS
    return
