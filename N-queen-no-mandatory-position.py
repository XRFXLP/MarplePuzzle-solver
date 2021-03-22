from functools import reduce
def nQueen(n):
    print(n)
    if n == 1:  return [0]
    if n <= 3:  return []
    if n %2 == 0 and n % 6 != 2:
        k = reduce(lambda x, y:x+y, [[(i - 1, 2*i - 1), (n//2 + i - 1, 2*i - 2)] for i in range(1, n//2 + 1)])
        return [i[1] for i in sorted(k, key = lambda x: x[0])]
    elif n % 2 == 0:
        k = reduce(lambda x, y: x + y, [[(i - 1, (2*(i - 1) + n//2 - 1)%n), (n - i, n - (2*(i - 1) + n//2 - 1)%n - 1)] for i in range(1, n//2 + 1)])
        return [i[1] for i in sorted(k, key = lambda x: x[0])]
    else:
        return nQueen(n - 1) + [n - 1]
