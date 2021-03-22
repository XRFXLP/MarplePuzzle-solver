'''
An efficient simple program to solve sliding puzzle game of variable sizes
'''

from copy import deepcopy
from functools import reduce
from time import sleep
class node:
    def __init__(self, loc):
        self.loc = loc
        self.parent = None
    def __eq__(self, other):
        return self.loc == other.loc
    def __hash__(self):
        return hash(self.loc)

def simpleMove(board, a, b, moves):
    if board[a[0]][a[1]] == 0 or board[b[0]][b[1]] == 0:
        if board[a[0]][a[1]] == 0:
            moves.append(board[b[0]][b[1]])
        else:
            moves.append(board[a[0]][a[1]])
    temp = board[b[0]][b[1]]
    board[b[0]][b[1]] = board[a[0]][a[1]]
    board[a[0]][a[1]] = temp
    return board

md = lambda x, y:abs(x[0] - y[0]) + abs(x[1] - y[1])
m = lambda lis,goal:lis.pop(lis.index(min(lis,  key = lambda x:md(x.loc, goal.loc))))

def neighbours(now, intheBoard):
    now = now.loc
    options = []
    for i in (-1, 0), (1, 0), (0, 1), (0, -1):
        a = now[0] + i[0]
        b = now[1] + i[1]
        if a >= 0 and a < len(intheBoard) and b >= 0 and b < len(intheBoard[0]):
            options.append(node((a, b)))
    return options

def pathConstruct(Node):
    if not Node:    return None
    path = []
    count = 0
    while Node:
        path.append(Node.loc)
        Node = Node.parent
        count += 1
    return tuple(path[::-1])

def path(p1,p2, visited, board):
    if p1 == p2:
        return (p1, 4343, 343)[:1]
    a, b = node(p1), node(p2)
    YU = []
    YUS = set()
    for i in neighbours(a, board):
        if i not in visited:
            i.parent = a
            YU.append(i)
            YUS.add(i)  
    visited.add(a)
    A = m(YU, b)
    YUS.discard(A)
    
    while True:
        if A.loc == b.loc or not A: return pathConstruct(A)
        visited.add(A)
        for j in neighbours(A, board):
            if j not in visited and j not in YUS:
                j.parent = A
                YU.append(j)
                YUS.add(j)
        A = m(YU,b)
        YUS.discard(A)
def posOf(x, board):
    return [(i, j) for j in range(len(board[0])) for i in range(len(board)) if board[i][j] == x][0]



def mainMove(From, to, board, protected, moves):
    if From == to:  return
    LL = deepcopy(protected)
    Path = path(From, to,LL, board)
    current = From
    for i in range(1, len(Path)):
        p2 = Path[i]
        zPos = posOf(0, board)
        pPath = list(path(p2, zPos, set([node(current)]).union(protected),board)[::-1])
        pPath.append((current[0], current[1]))
        for i in range(len(pPath) - 1):
            board = simpleMove(board, pPath[i], pPath[i + 1], moves)
        current = p2

def solvable(matrix):
    board = reduce(lambda a, b: a + b, matrix)
    count = sum([sum([1 for j in range(i + 1, len(board)) if board[j] < board[i] and board[j] != 0]) for i in range(len(board))])
    g = len(matrix[0])
    r = len(matrix) - posOf(0, matrix)[0]
    if not any([g % 2 == 1 and count % 2 == 0, g % 2 == 0 and r % 2 == 0 and count % 2 == 1,g % 2 == 0 and r % 2 == 1 and count % 2 == 0 ]):
        return False
    return True

def pos(count, originalLength, depth):
    return ((count - 1)//originalLength - (depth - 1), (count - 1)%originalLength - (depth - 1))

#lastMoved is supposed to be reversed
def slider(matrix, count, lastMoved, direction, protected, moves, depth):
    blanks = [(i[0] + 1, i[1]) if direction == 'd' else (i[0], i[1] + 1)  for i in lastMoved[1:]]
    moved = []
    flag = 0
    if direction == 'l' and len(matrix) == 3:
        blanks = [(1, 2)]
        flag = 1
        lastMoved = lastMoved[::-1]
    i = 2
    if flag == 0:
        protected.discard(node(lastMoved[i - 1]))
        mainMove(lastMoved[i - 1], blanks[i - 2], matrix, protected, moves)
        moved.append(blanks[i - 2])
        for j in range(1, i):
            protected.discard(node(lastMoved[i - 1 - j]))
            mainMove(lastMoved[i - 1 - j], lastMoved[i - j], matrix, protected, moves)
            moved.append(lastMoved[i - j])
        protected.discard(node(posOf(count, matrix)))
        mainMove(posOf(count, matrix), lastMoved[i - 1 - j], matrix, protected, moves)
        moved.append(lastMoved[i - 1 - j])
    else:
        protected.discard(node(lastMoved[i - 2]))
        mainMove(lastMoved[i - 2], blanks[i - 2], matrix, protected, moves)
        moved.append(blanks[i - 2])
        for j in range(1, len(lastMoved)):
            protected.discard(node(lastMoved[j]))
            mainMove(lastMoved[j], lastMoved[j - 1], matrix, protected, moves)
            moved.append(lastMoved[j - 1])
        protected.discard(node(posOf(count, matrix)))
        mainMove(posOf(count, matrix), lastMoved[-1], matrix, protected, moves)
        moved.append(lastMoved[-1])
    for i in moved[::-1]:
        to = pos(matrix[i[0]][i[1]], len(matrix) + (depth - 1), depth)
        mainMove(i,to , matrix, protected, moves)
        protected.add(node(to)) 
    
    
def slide_puzzle(matrix, ll = 1, depth = 1):
    if depth == 1 and not solvable(matrix):
        return None
    e = set()
    count = deepcopy(ll)
    moves = []
    B = len(matrix)
    if B == 1:
        return 
    lastMoved = []
    
    for j in range(B - 1):
        a = posOf(count, matrix)
        d = pos(count, B + (depth - 1), depth)
        mainMove(a, d, matrix, e, moves)
        lastMoved.append(d)
        e.add(node(d))
        count += 1
    p_ = (pos(count, B + (depth - 1), depth)[0] + 1,pos(count, B + (depth - 1), depth)[1] - 1)
    if B == 2:
        simpleMove(matrix,pos(count, B + (depth - 1), depth) , posOf(count, matrix), moves)
        count += depth
        simpleMove(matrix,pos(count, B + (depth - 1), depth) , posOf(count, matrix), moves)
        return moves



    tea = (posOf(count, matrix)[0] - 1, posOf(count, matrix)[1])
    if  tea == pos(count, B + (depth - 1), depth) and matrix[tea[0]][tea[1]] == 0:
        simpleMove(matrix, posOf(count, matrix), pos(count, B + (depth - 1), depth), moves)
    if posOf(count, matrix) != pos(count, B + (depth - 1), depth):
        mainMove(posOf(count, matrix),p_ , matrix, e, moves)
        e.add(node(p_))
        slider(matrix, count,lastMoved[::-1], 'd', e, moves, depth)


    count += depth
    if B != 3:
        lastMoved = []
    else:
        c = posOf(count - depth, matrix)
    for j in range(1, B - 1):
        a = posOf(count, matrix)
        d = pos(count, B + (depth - 1), depth)
        mainMove(a, d, matrix, e, moves)
        lastMoved.append(d)
        e.add(node(d))
        count += B + (depth - 1)
    
    p_ = (pos(count, B + (depth - 1), depth)[0] - 1,pos(count, B + (depth - 1), depth)[1] + 1)
    tea = (posOf(count, matrix)[0], posOf(count, matrix)[1] - 1)
    if  tea == pos(count, B + (depth - 1), depth) and matrix[tea[0]][tea[1]] == 0:
        simpleMove(matrix, posOf(count, matrix), pos(count, B + (depth - 1), depth), moves)
    if B == 3:
        lastMoved = [c] + lastMoved[:-1][::-1] + [d]

    if posOf(count, matrix) != pos(count, B + (depth - 1), depth):
        mainMove(posOf(count, matrix),p_ , matrix, e, moves)
        e.add(node(p_))
        slider(matrix, count,lastMoved[::-1], 'l', e, moves, depth)
    newMatrix = [i[1:] for i in matrix[1:]]
    moves += slide_puzzle(newMatrix, ll + B + depth, depth + 1)
    return moves
