graph = [[], [], []]
graph[0].append((1, 4))  # 终点、权重
graph[1].append((2, 3))
for start, edges in enumerate(graph):
    for end, weight in edges:
        print(f"{start} -> {end}，权重 {weight}")
