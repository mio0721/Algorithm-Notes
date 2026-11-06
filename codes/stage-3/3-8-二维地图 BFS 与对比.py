# 二维地图 BFS 与对比
# Python 3；直接运行文件，修改示例数据可继续练习。
# 起点距离设为0并入队。

from collections import deque
grid = ['....', '.##.', '....']
R, C = (len(grid), len(grid[0]))
dist = [[-1] * C for _ in range(R)]
queue = deque()
if grid[0][0] != '#':
    dist[0][0] = 0
    queue.append((0, 0))
# 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
while queue:
    # 读取先进先出的队首，保持发现的层次顺序。
    r, c = queue.popleft()
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = (r + dr, c + dc)
        if 0 <= nr < R and 0 <= nc < C and (grid[nr][nc] != '#') and (dist[nr][nc] == -1):
            # 四邻域每走一步代价相同，距离比父格多1。
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print('steps=', dist[-1][-1])
