from collections import deque
g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
dist, parent = [-1] * 10, [-1] * 10
dist[0], queue = 0, deque([0])
while queue:
    u = queue.popleft()
    for v in g[u]:
        if dist[v] == -1:
            dist[v], parent[v] = dist[u] + 1, u
            queue.append(v)
if dist[9] == -1:
    print("unreachable")
else:
    path, node = [], 9
    while node != -1:
        path.append(chr(65 + node))
        node = parent[node]
    print(path[::-1], "steps=", dist[9])
