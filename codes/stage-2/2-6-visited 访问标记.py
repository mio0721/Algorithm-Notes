from collections import deque
graph = [[1, 2], [0, 2], [0, 1]]
visited = [False] * len(graph)
pending = deque([0])
visited[0] = True
while pending:
    node = pending.popleft()
    print("访问", chr(ord("A") + node))
    for neighbor in graph[node]:
        if not visited[neighbor]:
            visited[neighbor] = True
            pending.append(neighbor)
