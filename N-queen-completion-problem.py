def queens(position, size):
    to = lambda x: (0 if x[1]=='0' else size - int(x[1]), ord(x[0]) - 97)
    po = lambda x: f'{chr(97 + x[1])}{(size - x[0])%10}'
    position = to(position)
    is_possible=lambda p, v: not any(i[0]==p[0]or i[1]==p[1] or sum(i)==sum(p)or i[1]-i[0] == p[1] - p[0] for i in v)
    visited = set([position])
    def DFS(row, visited):
        print(len(visited), size - 1)
        if len(visited) == size:            return map(po, sorted(visited))
        if row == position[0]:              return DFS(row+1, visited)
        for i in range(size):
            if is_possible((row, i), visited):
                V = DFS(row + 1, visited | {(row, i)})
                if V:                   return V
        return False
    return ','.join([*DFS(0, visited)])
