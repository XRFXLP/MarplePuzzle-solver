import copy 
def dr(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    if x == 1:  return 'N'
    elif x == -1:   return 'S'
    elif y == 1:    return 'W'
    else:   return 'E'
    
class Node:
    def __init__(self, loc):
        self.loc = loc
        self.parent = None
        self.inte = 0
    def __eq__(self, other):
        return self.loc == other.loc
    def __hash__(self):
        return hash(self.loc)
    def __gt__(self, other):
        return self.loc[0] > other.loc[0]
    
def rot(x, interval):
    if x == 0:  return 0
    class1 = [4, 8, 1, 2]
    class2 = [3, 6, 12, 9]
    class3 = [7, 14, 13, 11]
    class4 = [5, 10]
    if x in class1: return class1[(class1.index(x) + interval)%4]
    elif x in class2:   return class2[(class2.index(x) + interval)%4]
    elif x in class3:   return class3[(class3.index(x) + interval)%4]
    else:   return class4[(class4.index(x) + interval)%2]
    
def n(matrix, cur, h, w, interval):
    a, b = cur.loc
    options = []    
    for i, j, k, l in (a - 1, b, 2, 0), (a + 1, b, 0, 2), (a, b-1, 3, 1), (a, b + 1, 1, 3):
        if min(i, j) > -1 and j < w and i < h and matrix[i][j] != 'W':
            t = bin(rot(matrix[i][j], interval))[2:]
            s = bin(rot(matrix[a][b], interval))[2:]
            if ('0'*(4 - len(t)) + t)[k] != '1' and ('0'*(4 - len(s)) + s)[l] != '1':
                options.append(Node((i, j)))
    return options
def maze_solvr(X):
    X = [list(i) for i in X]
    H = len(X)
    W = len(X[0])
    
    for i in range(H):
        for j in range(W):
            if X[i][j] == 'B':
                X[i][j] = 0
                st = Node((i, j))
            elif X[i][j] == 'X':
                X[i][j] = 0
                en = (i, j)
            elif X[i][j] == 15:
                X[i][j] = 'W'

    interval = 0
    Queue = [st]
    visited, fr, pfr = set(), [] ,[]
    x = 0
    count  = 0
    while True:
        x += 1
        i = Queue.pop()
        
        if type(i) == tuple:
            i = Node(i)
            
        if i.loc == en:
            return i
        for j in n(X, i, H, W, interval):
            if j.loc == en:
                j.parent = i
                j.inte = interval
                return j
            if j not in visited:
                j.parent = i
                j.inte = interval
                Queue.append(j)
        visited.add(i)
        fr.append(i)
        if len(Queue) == 0:
            Queue = fr
            if fr == []:
                return None
            if sorted([i.loc for i in fr]) == sorted([i.loc for i in pfr]):
                count += 1
                if count > 4:
                    break
            pfr = copy.copy(fr)
            interval += 1
            fr = []
            x = 0
            
def maze_solver(X):
    t = maze_solvr(X)
    if not t:   return None
    a,b = [], []
    if t:
        while t:
            a.append(t.loc)
            b.append(t.inte)
            t = t.parent
    a = a[::-1]
    b = b[::-1]
    di = []
    t = ''
    for i in range(1, len(b)):
        if b[i] - b[i - 1] >= 1:
            di.append(t)
            for _ in range(b[i-1], b[i] - 1):
                di.append('')
            t = ''
        t += dr(a[i-1], a[i])
    di.append(t)
    return di
