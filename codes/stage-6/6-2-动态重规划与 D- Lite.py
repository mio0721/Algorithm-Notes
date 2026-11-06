# 动态重规划与 D* Lite
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先从目标反向维护“走到目标还要多少代价”。

import math
import heapq

# 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
class DStarLite:
    """四邻域无向栅格；保留g/rhs，采用惰性删除过滤过期队列项。"""

    # 初始化本对象保存的状态，后续方法将共同使用这些成员。
    def __init__(self, grid, start, goal):
        if not grid or not grid[0] or any((len(row) != len(grid[0]) for row in grid)):
            # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
            raise ValueError('地图必须是非空矩形')
        if any((not (0 <= r < len(grid) and 0 <= c < len(grid[0])) for r, c in (start, goal))):
            raise ValueError('起终点不能超出地图')
        if any((grid[r][c] == '#' for r, c in (start, goal))):
            raise ValueError('起终点必须可通行')
        self.grid = [list(row) for row in grid]
        self.start, self.goal, self.last = (start, goal, start)
        self.km = 0
        # 目标的一跳前瞻代价固定为0，其余未建立的状态视为无穷大。
        self.g, self.rhs = ({}, {goal: 0})
        self.heap, self.pending = ([], {})
        self.push(goal)

    # 计算两格之间的曼哈顿距离，作为一致的剩余代价下界。
    def h(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 读取状态表；尚未建立记录的顶点统一视为无穷大。
    def value(self, table, u):
        return table.get(u, math.inf)

    # 计算两个字段组成的关键字，先比较第一项，相等时再比较第二项。
    def key(self, u):
        best = min(self.value(self.g, u), self.value(self.rhs, u))
        return (best + self.h(self.start, u) + self.km, best)

    # 枚举地图内的四个相邻格；是否能穿过障碍由边代价函数进一步决定。
    def neighbors(self, u):
        r, c = u
        return [(a, b) for a, b in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)) if 0 <= a < len(self.grid) and 0 <= b < len(self.grid[0])]

    # 任一端点是障碍时边代价为无穷大，否则四邻域一步代价为1。
    def cost(self, u, v):
        return math.inf if self.grid[u[0]][u[1]] == '#' or self.grid[v[0]][v[1]] == '#' else 1

    # 登记顶点当前有效关键字并压入最小堆，旧副本暂时保留。
    def push(self, u):
        key = self.key(u)
        self.pending[u] = key
        # 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
        heapq.heappush(self.heap, (key, u))

    # 在查看堆顶前丢弃过期副本，只返回当前有效的最小关键字。
    def top(self):
        # 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
        while self.heap and self.pending.get(self.heap[0][1]) != self.heap[0][0]:
            # 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
            heapq.heappop(self.heap)
        return self.heap[0][0] if self.heap else (math.inf, math.inf)

    # 重新计算一跳前瞻代价；只有g与rhs不一致的顶点才需要进入修复队列。
    def update(self, u):
        if u != self.goal:
            self.rhs[u] = min((self.cost(u, v) + self.value(self.g, v) for v in self.neighbors(u)), default=math.inf)
        # 删除当前有效队列登记；堆中的历史副本由top惰性丢弃。
        self.pending.pop(u, None)
        if self.value(self.g, u) != self.value(self.rhs, u):
            self.push(u)

    # 传播不一致状态，直到当前位置一致，且队列没有更小关键字需要处理。
    def repair(self):
        while self.top() < self.key(self.start) or self.value(self.rhs, self.start) != self.value(self.g, self.start):
            # 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
            old, u = heapq.heappop(self.heap)
            # 删除当前有效队列登记；堆中的历史副本由top惰性丢弃。
            self.pending.pop(u, None)
            # 起点移动后关键字可能变大，先重新计算并按新键入队。
            if old < self.key(u):
                self.push(u)
            elif self.value(self.g, u) > self.value(self.rhs, u):
                self.g[u] = self.value(self.rhs, u)
                for p in self.neighbors(u):
                    self.update(p)
            else:
                # 旧代价失效时先设为无穷大，再重新传播，不直接把坏状态当作有效答案。
                self.g[u] = math.inf
                # 重新检查当前顶点是否一致；不一致才进入修复队列。
                self.update(u)
                for p in self.neighbors(u):
                    self.update(p)

    # 修改一个格子的占据状态，并更新它及相邻格受影响的边代价。
    def change(self, cell, blocked):
        if cell in (self.start, self.goal):
            # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
            raise ValueError('不能把当前位置或目标设为障碍')
        self.grid[cell[0]][cell[1]] = '#' if blocked else '.'
        for u in [cell] + self.neighbors(cell):
            # 重新检查当前顶点是否一致；不一致才进入修复队列。
            self.update(u)

    # 起点移动后维护关键字偏移km，保留并复用原有搜索数据。
    def move(self, start):
        # 移动起点时累加启发式偏移，复用原队列和搜索状态。
        self.km += self.h(self.last, start)
        self.start = self.last = start

    # 沿边代价加后继g最小的方向提取路线，检测无路与异常循环。
    def path(self):
        if not math.isfinite(self.value(self.rhs, self.start)):
            return []
        route, seen = ([self.start], {self.start})
        while route[-1] != self.goal:
            u = route[-1]
            v = min(self.neighbors(u), key=lambda v: self.cost(u, v) + self.value(self.g, v))
            if v in seen or not math.isfinite(self.cost(u, v) + self.value(self.g, v)):
                return []
            route.append(v)
            seen.add(v)
        return route

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    grid = ['.........', '.###.###.', '...#.....', '...#.###.', '.........', '..###....']
    planner = DStarLite(grid, (0, 0), (5, 8))
    planner.repair()
    before = planner.path()
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('initial:', before)
    changed = before[len(before) // 2]
    planner.change(changed, True)
    planner.repair()
    print('repaired:', planner.path())
    planner.change(changed, False)
    planner.move(before[1])
    planner.repair()
    print('restored and moved:', planner.path())
if __name__ == '__main__':
    main()
