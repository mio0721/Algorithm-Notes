g = [[1, 2], [3, 4], [5, 6], [7], [8, 5], [], [9], [], [9], []]
path, on_path = [], set()
def dfs(u):
    path.append(u)
    on_path.add(u)
    if u == 9:
        print([chr(65 + v) for v in path])
    else:
        for v in g[u]:
            if v not in on_path:
                dfs(v)
    path.pop()
    on_path.remove(u)
dfs(0)
