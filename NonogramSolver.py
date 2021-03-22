'''
A simple program to solve 15 by 15 nonogram puzzle
'''
from functools import lru_cache

def pds(s, size):
    return s.zfill(size).replace('0', ' ')

def pretty_print(board, clues):
    mH = len(max(clues[0], key=len))
    mV = len(max(clues[1], key=len))
    L = mH + len(board)
    W = mV + len(board[0])
    COL = zip(*[pds(''.join(map(str, i)), mH) for i in clues[0]])
    ROW = [' '.join([*pds(''.join(map(str, i)), mV)]) for i in clues[1]]
    print('\n'.join(' '*(len(ROW[0])) + ' '.join(i) for i in COL))


    n = [['⬜' if j == 0 else '⬛' if j == 1 else '❌' for j in i] for i in board]
    print('\n'.join(j + ''.join(i) for i,j in zip(n, ROW)))

@lru_cache(maxsize=None)
def all_configurations(vec, clue):
    K = [len(clue)]
    limits = [(2 * sum(clue[:i]), len(vec) - (sum(clue[i:]) + K[0] - i - 1)) for i in range(K[0])]
    @lru_cache(maxsize=None)
    def recurse(v_ind, c_ind):
        if c_ind >= K[0] or v_ind >= len(vec):
            return ((),)
        all_config = ()
        u = (1, ) * clue[c_ind] + ((0,) if c_ind != K[0] - 1 else ())
        
        for i in range(v_ind, limits[c_ind][1] + 1):
            k = (0, ) * (i - v_ind) + u
            all_config += tuple([k + config for config in recurse(i + clue[c_ind] + 1, c_ind + 1)])
        return all_config

    return tuple([config + ((0,) * (len(vec) - len(config))) for config in recurse(0, 0)])
    

def translate(dir, i, confirmed):
    return {(i, j) if dir == 'H' else (j, i) for j in confirmed}

def simple_box(board, all_clues):
    def confirmed_blocks(i, dir, vec, clue):
        all_config = all_configurations(vec, clue)
        MEMORY[(i, dir)] = all_config

        return [i for i in range(len(all_config[0]))if all(x[i] == 1 for x in all_config)]

    for dir, clues in zip('VH', all_clues):
        limit = len(board) if dir == 'H' else len(board[0])
        for i in range(limit):
            vec = tuple([row[i] for row in board]) if dir == 'V' else tuple(board[i])
            for y, x in translate(dir, i, confirmed_blocks(i, dir, vec, clues[i])):
                board[y][x] = 1
    
MEMORY = {}

@lru_cache(maxsize=None)
def vec_crosses(i, dir, vec, clue):
    MEMORY[(i, dir)] = [x for x in MEMORY[(i,dir)] if all([True if j == 0 else i == 0 if j == -1 else i == 1 for i, j in zip(x, vec)])]
    all_config = zip(*MEMORY[(i, dir)])
    crosses, confirmed = (), ()
    for i, j in enumerate(all_config):
        if vec[i] != 0:
            continue
        W = sum(j)
        if W == 0 and vec[i] != -1:
            crosses += (i, )
        elif vec[i] != 1 and W == len(j):
            confirmed += (i, )
    return crosses, confirmed

def forcing(board, all_clues):
    for dir, clues in zip('VH', all_clues):
        limit = len(board) if dir == 'H' else len(board[0])
        for i in range(limit):
            vec = tuple([row[i] for row in board]) if dir == 'V' else tuple(board[i])
            if 0 not in vec:
                continue
            crosses_l, confirmed_l = vec_crosses(i, dir, vec, clues[i])
            if crosses_l:
                for y, x in translate(dir, i, crosses_l):
                    board[y][x] = -1
            if confirmed_l:
                for y, x in translate(dir, i, confirmed_l):
                    board[y][x] = 1

def solve(clues, W = 15, H = 15):
    global MEMORY
    MEMORY = {}
    board = [[0 for i in range(W)] for j in range(H)]
    simple_box(board, clues)
    while next((1 for i in range(W) for j in range(H) if board[j][i] == 0), None):
        forcing(board, clues)
    return tuple(map(lambda x: tuple([0 if i == -1 else 1 for i in x]), board))
