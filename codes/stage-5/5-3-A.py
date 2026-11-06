# A*
# Python 3；直接运行文件，修改示例数据可继续练习。
# 记录已经走到当前格花了多少。

import math
import heapq

# 在单位四邻域地图上搜索；h取曼哈顿距离，或取0进行一致代价搜索。
def grid_astar(grid, start, goal, heuristic=True):
    if not grid or not grid[0] or any((len(row) != len(grid[0]) for row in grid)):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('地图必须是非空矩形')
    rows, cols = (len(grid), len(grid[0]))
    if any((not (0 <= r < rows and 0 <= c < cols) for r, c in (start, goal))):
        raise ValueError('起终点不能超出地图')
    if grid[start[0]][start[1]] == '#' or grid[goal[0]][goal[1]] == '#':
        return []
    # 四邻域单位步长使用曼哈顿距离作为剩余代价下界；h=0退化为一致代价搜索。
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1]) if heuristic else 0
    pending = [(h(start), 0, start)]
    distance, parent, expanded = ({start: 0}, {}, set())
    # 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while pending:
        # 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
        _, cost, u = heapq.heappop(pending)
        if cost != distance[u]:
            continue
        expanded.add(u)
        if u == goal:
            # 四邻域单位步长使用曼哈顿距离作为剩余代价下界；h=0退化为一致代价搜索。
            path = [u]
            while u != start:
                # 只在路线改善时更新前驱，恢复时才有完整可行的父链。
                u = parent[u]
                path.append(u)
            # 把反向收集的数据恢复为实际输出顺序。
            path.reverse()
            return path
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            v = (u[0] + dr, u[1] + dc)
            if 0 <= v[0] < rows and 0 <= v[1] < cols and (grid[v[0]][v[1]] != '#'):
                candidate = cost + 1
                if candidate < distance.get(v, math.inf):
                    # 只在路线改善时更新前驱，恢复时才有完整可行的父链。
                    distance[v], parent[v] = (candidate, u)
                    # 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
                    heapq.heappush(pending, (candidate + h(v), candidate, v))
    return []

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    grid = ['.........', '.###.###.', '...#.....', '...#.###.', '.........', '..###....']
    route = grid_astar(grid, (0, 0), (5, 8))
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('steps:', len(route) - 1 if route else 'unreachable')
    print(route)
if __name__ == '__main__':
    main()
