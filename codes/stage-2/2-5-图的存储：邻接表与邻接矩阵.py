graph = [[] for _ in range(8)]
for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7), (4, 7)]:
    graph[a].append(b)
    graph[b].append(a)
for node, neighbors in enumerate(graph):
    print(f"{node}: {neighbors}")
