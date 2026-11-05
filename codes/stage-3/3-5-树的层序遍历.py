from collections import deque
children = [[1, 2], [3, 4], [5, 6], [7], [8], [], [9], [], [], []]
queue = deque([0])
while queue:
    level = []
    for _ in range(len(queue)):
        node = queue.popleft()
        level.append(node + 1)
        queue.extend(children[node])
    print(level)
