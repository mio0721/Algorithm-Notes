"""Runnable demonstrations for newly added lessons."""
PY={
'1.7':'''s = "abcabcbbd"
last = {}
left = best = 0
for right, ch in enumerate(s):
    if ch in last:
        left = max(left, last[ch] + 1)
    last[ch] = right
    best = max(best, right - left + 1)
print(best)''',
'1.8':'''a = [9, 3, 7, 1, 8, 2, 6, 4, 5]
for i in range(1, len(a)):
    value, j = a[i], i - 1
    while j >= 0 and a[j] > value:
        a[j + 1] = a[j]
        j -= 1
    a[j + 1] = value
print(a)''',
'3.1':'''g = [[1, 2], [0, 3], [0], [1]]
seen = set()
def dfs(u):
    seen.add(u)
    print(chr(65 + u), end=" ")
    for v in g[u]:
        if v not in seen:
            dfs(v)
dfs(0)
print()''',
'3.2':'''g = [[1, 2], [0, 3], [0], [1]]
seen, stack = {0}, [0]
while stack:
    u = stack.pop()
    print(chr(65 + u), end=" ")
    for v in reversed(g[u]):
        if v not in seen:
            seen.add(v)
            stack.append(v)
print()''',
'3.3':'''g = [[1, 2], [3], [3], []]
path, on_path = [], set()
def dfs(u):
    path.append(u)
    on_path.add(u)
    if u == 3:
        print([chr(65 + v) for v in path])
    else:
        for v in g[u]:
            if v not in on_path:
                dfs(v)
    path.pop()
    on_path.remove(u)
dfs(0)''',
'3.4':'''from collections import deque
g = [[1, 2], [0, 3], [0], [1]]
seen, queue = {0}, deque([0])
while queue:
    u = queue.popleft()
    print(chr(65 + u), end=" ")
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            queue.append(v)
print()''',
'3.5':'''from collections import deque
children = [[1, 2], [3, 4], [], [], []]
queue = deque([0])
while queue:
    level = []
    for _ in range(len(queue)):
        node = queue.popleft()
        level.append(node + 1)
        queue.extend(children[node])
    print(level)''',
'3.6':'''from collections import deque
g = [[1, 2], [0, 3], [0, 3], [1, 2]]
dist, parent = [-1] * 4, [-1] * 4
dist[0], queue = 0, deque([0])
while queue:
    u = queue.popleft()
    for v in g[u]:
        if dist[v] == -1:
            dist[v], parent[v] = dist[u] + 1, u
            queue.append(v)
if dist[3] == -1:
    print("unreachable")
else:
    path, node = [], 3
    while node != -1:
        path.append(chr(65 + node))
        node = parent[node]
    print(path[::-1], "steps=", dist[3])''',
'3.7':'''grid = ["....", ".##.", "...."]
R, C = len(grid), len(grid[0])
seen = set()
def dfs(r, c):
    if not (0 <= r < R and 0 <= c < C) or grid[r][c] == "#" or (r, c) in seen:
        return False
    seen.add((r, c))
    if (r, c) == (R - 1, C - 1):
        return True
    return any(dfs(r + dr, c + dc) for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)])
print("reachable" if dfs(0, 0) else "unreachable")''',
'3.8':'''from collections import deque
grid = ["....", ".##.", "...."]
R, C = len(grid), len(grid[0])
dist = [[-1] * C for _ in range(R)]
queue = deque()
if grid[0][0] != "#":
    dist[0][0] = 0
    queue.append((0, 0))
while queue:
    r, c = queue.popleft()
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and dist[nr][nc] == -1:
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
print("steps=", dist[-1][-1])'''
}
def code_for(id):
    import re
    from textwrap import indent
    from graph_examples import graph_for
    from readable_cpp import body

    python = PY[id]
    if id in ('3.1', '3.2', '3.3', '3.4', '3.5', '3.6'):
        graph, _, _ = graph_for(id)
        variable = 'children' if id == '3.5' else 'g'
        python = re.sub(r'^' + variable + r' = .*$',
                        variable + ' = ' + repr(graph), python,
                        count=1, flags=re.M)
        if id == '3.3':
            python = python.replace('u == 3', 'u == 9')
        if id == '3.6':
            python = (python.replace('[-1] * 4', '[-1] * 10')
                      .replace('dist[3]', 'dist[9]').replace('[], 3', '[], 9'))

    includes = ['iostream', 'vector', 'string', 'queue', 'stack',
                'unordered_map', 'functional', 'algorithm']
    header = ''.join('#include <' + name + '>\n' for name in includes)
    header += 'using namespace std;\n\n'
    cpp = header + 'int main() {\n' + indent(body(id), '    ')
    cpp += '\n    return 0;\n}\n'
    return cpp, python + '\n'
