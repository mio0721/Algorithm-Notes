from collections import deque
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
print("steps=", dist[-1][-1])
