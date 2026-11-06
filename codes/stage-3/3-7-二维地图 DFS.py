# 二维地图 DFS
# Python 3；直接运行文件，修改示例数据可继续练习。
# 从起点进入格子并标记。

grid = ['....', '.##.', '....']
R, C = (len(grid), len(grid[0]))
# 访问标记初始为空或全为假，表示还没有发现节点。
seen = set()

# 进入节点后标记，再逐个递归访问尚未发现的邻居。
def dfs(r, c):
    # 先检查坐标合法，再检查障碍与访问状态，防止越界。
    if not (0 <= r < R and 0 <= c < C) or grid[r][c] == '#' or (r, c) in seen:
        return False
    seen.add((r, c))
    if (r, c) == (R - 1, C - 1):
        # 找到一条路线即返回成功；这不保证它是最短路线。
        return True
    return any((dfs(r + dr, c + dc) for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]))
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print('reachable' if dfs(0, 0) else 'unreachable')
