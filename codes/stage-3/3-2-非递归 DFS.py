g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
seen, stack = {0}, [0]
while stack:
    u = stack.pop()
    print(chr(65 + u), end=" ")
    for v in reversed(g[u]):
        if v not in seen:
            seen.add(v)
            stack.append(v)
print()
