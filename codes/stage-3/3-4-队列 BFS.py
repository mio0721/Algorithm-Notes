from collections import deque
g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
seen, queue = {0}, deque([0])
while queue:
    u = queue.popleft()
    print(chr(65 + u), end=" ")
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            queue.append(v)
print()
