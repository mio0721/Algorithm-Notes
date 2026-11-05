g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
seen = set()
def dfs(u):
    seen.add(u)
    print(chr(65 + u), end=" ")
    for v in g[u]:
        if v not in seen:
            dfs(v)
dfs(0)
print()
