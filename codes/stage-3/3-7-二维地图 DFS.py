grid = ["....", ".##.", "...."]
R, C = len(grid), len(grid[0])
seen = set()
def dfs(r, c):
    if not (0 <= r < R and 0 <= c < C) or grid[r][c] == "#" or (r, c) in seen:
        return False
    seen.add((r, c))
    if (r, c) == (R - 1, C - 1):
        return True
    return any(dfs(r + dr, c + dc) for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)])
print("reachable" if dfs(0, 0) else "unreachable")
