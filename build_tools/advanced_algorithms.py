"""Reference algorithms and optional state events for stages 4–6."""
import heapq
import math
import random
from collections import deque


def emit_state(emit, text, cells=(), **visual):
    if emit is not None:
        frame = dict(text=text, cells=[str(x) for x in cells], active=[])
        frame.update(visual)
        emit(frame)


def subsets(nums, emit=None):
    answer, path = [], []

    def visit(index):
        answer.append(path.copy())
        emit_state(emit, '保存当前子集，再尝试后续元素。', path)
        for i in range(index, len(nums)):
            path.append(nums[i])
            emit_state(emit, f'选择下标 {i} 的 {nums[i]}。', path)
            visit(i + 1)
            path.pop()
            emit_state(emit, '撤销最后一次选择。', path)

    visit(0)
    return answer


def select_intervals(intervals, emit=None):
    if any(end < start for start, end in intervals):
        raise ValueError('区间终点不能小于起点')
    chosen, end_time = [], -math.inf
    for start, end in sorted(intervals, key=lambda pair: (pair[1], pair[0])):
        take = start >= end_time
        if take:
            chosen.append((start, end))
            end_time = end
        emit_state(emit, f'检查 [{start},{end})：' + ('选择' if take else '与已选区间冲突'),
                   [f'[{a},{b})' for a, b in chosen])
    return chosen


def merge_sort(nums, emit=None):
    a = list(nums)

    def sort(left, right):
        if right - left <= 1:
            return
        middle = (left + right) // 2
        sort(left, middle)
        sort(middle, right)
        merged, i, j = [], left, middle
        while i < middle and j < right:
            if a[i] <= a[j]:  # 相等时取左边，维持稳定性。
                merged.append(a[i])
                i += 1
            else:
                merged.append(a[j])
                j += 1
        a[left:right] = merged + a[i:middle] + a[j:right]
        emit_state(emit, f'合并 [{left},{middle}) 和 [{middle},{right})。', a,
                   indexed=True, range=[left, right - 1])

    emit_state(emit, '初始数组。', a, indexed=True)
    sort(0, len(a))
    return a


def climb_stairs(n, emit=None):
    if n < 0:
        raise ValueError('台阶数必须非负')
    dp = [0] * (n + 1)
    dp[0] = 1
    emit_state(emit, 'dp[0]=1：什么也不做也是一种到达方式。', dp, indexed=True)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)
        emit_state(emit, f'dp[{i}]={dp[i]}，由最后一步走 1 或 2 级分类。', dp,
                   indexed=True, active=[i])
    return dp[n]


def knapsack(weights, values, capacity, emit=None):
    if len(weights) != len(values) or capacity < 0 or any(w <= 0 for w in weights):
        raise ValueError('重量必须为正，容量非负，重量与价值数量一致')
    dp = [0] * (capacity + 1)
    emit_state(emit, '容量上限模型：允许不装，所有初值为 0。', dp, indexed=True)
    for item, (weight, value) in enumerate(zip(weights, values)):
        for room in range(capacity, weight - 1, -1):
            old = dp[room]
            dp[room] = max(dp[room], dp[room - weight] + value)
            emit_state(emit, f'物品 {item}，容量 {room}：max({old},'
                       f'{dp[room-weight]}+{value})={dp[room]}。', dp,
                       indexed=True, active=[room])
    return dp[capacity]


def lcs(first, second, emit=None):
    m, n = len(first), len(second)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            emit_state(emit, f'比较 {first[i-1]} 与 {second[j-1]}，dp[{i}][{j}]={dp[i][j]}。',
                       matrix=dp, rowLabels=['空'] + list(first),
                       colLabels=['空'] + list(second), matrixActive=[i, j])
    path, i, j = [], m, n
    while i and j:
        if first[i - 1] == second[j - 1]:
            path.append(first[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], ''.join(reversed(path))


def components(graph, emit=None):
    seen, groups = set(), []
    for start in range(len(graph)):
        if start in seen:
            continue
        seen.add(start)
        pending, group = [start], []
        while pending:
            u = pending.pop()
            group.append(u)
            emit_state(emit, f'连通分量 {len(groups)+1} 发现节点 {u}。', group, highlight=group)
            for v in reversed(graph[u]):
                if v not in seen:
                    seen.add(v)
                    pending.append(v)
        groups.append(group)
    return groups


def dijkstra(graph, start, emit=None):
    if any(weight < 0 for row in graph for _, weight in row):
        raise ValueError('Dijkstra 不支持负边权')
    distance, parent = [math.inf] * len(graph), [-1] * len(graph)
    distance[start] = 0
    pending = [(0, start)]
    settled = set()
    while pending:
        cost, u = heapq.heappop(pending)
        if cost != distance[u]:
            continue
        settled.add(u)
        emit_state(emit, f'弹出当前最小有效距离：节点 {u}，距离 {cost}。',
                   [f'{i}: {d}' for i, d in enumerate(distance)], highlight=[u],
                   distances=list(distance), parents=list(parent), settled=sorted(settled))
        for v, weight in graph[u]:
            candidate = cost + weight
            if candidate < distance[v]:
                distance[v], parent[v] = candidate, u
                heapq.heappush(pending, (candidate, v))
                emit_state(emit, f'松弛 {u}→{v}，新距离 {candidate}。',
                           [f'{i}: {d}' for i, d in enumerate(distance)], highlight=[u, v],
                           distances=list(distance), parents=list(parent), settled=sorted(settled), updated=v)
    return distance, parent


def grid_astar(grid, start, goal, emit=None, heuristic=True):
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('地图必须是非空矩形')
    rows, cols = len(grid), len(grid[0])
    if any(not (0 <= r < rows and 0 <= c < cols) for r,c in (start,goal)):
        raise ValueError('起终点不能超出地图')
    if grid[start[0]][start[1]] == '#' or grid[goal[0]][goal[1]] == '#':
        return []
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1]) if heuristic else 0
    pending = [(h(start), 0, start)]
    distance, parent, expanded = {start: 0}, {}, set()
    def scores():
        return {f'{r},{c}': dict(w=1, g=distance.get((r,c),math.inf), h=h((r,c)),
                                f=distance.get((r,c),math.inf)+h((r,c)))
                for r in range(rows) for c in range(cols) if grid[r][c] != '#'}
    while pending:
        _, cost, u = heapq.heappop(pending)
        if cost != distance[u]:
            continue
        expanded.add(u)
        emit_state(emit, f'扩展 {u}：g={cost}，h={h(u)}，f={cost+h(u)}。',
                   grid=grid, start=start, goal=goal, current=u,
                   visited=list(expanded), frontier=[x[2] for x in pending], route=[],
                   scores=scores(), scoreKind='astar')
        if u == goal:
            path = [u]
            while u != start:
                u = parent[u]
                path.append(u)
            path.reverse()
            emit_state(emit, f'找到最短路，共 {len(path)-1} 步。', grid=grid,
                       start=start, goal=goal, visited=list(expanded), route=path,
                       scores=scores(), scoreKind='astar')
            return path
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            v = u[0] + dr, u[1] + dc
            if 0 <= v[0] < rows and 0 <= v[1] < cols and grid[v[0]][v[1]] != '#':
                candidate = cost + 1
                if candidate < distance.get(v, math.inf):
                    distance[v], parent[v] = candidate, u
                    heapq.heappush(pending, (candidate + h(v), candidate, v))
    emit_state(emit, '终点不可达。', grid=grid, start=start, goal=goal,
               visited=list(expanded), route=[], scores=scores(), scoreKind='astar')
    return []


def floyd_warshall(matrix, emit=None):
    d = [row.copy() for row in matrix]
    for k in range(len(d)):
        for i in range(len(d)):
            for j in range(len(d)):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        emit_state(emit, f'允许编号 0～{k} 的节点作为中转点。', matrix=d,
                   rowLabels=list(range(len(d))), colLabels=list(range(len(d))))
    if any(d[i][i] < 0 for i in range(len(d))):
        raise ValueError('检测到负环，不能直接把矩阵解释为有限最短距离')
    return d


def topological_sort(graph, emit=None):
    degree = [0] * len(graph)
    for row in graph:
        for v in row:
            degree[v] += 1
    pending = deque(i for i, d in enumerate(degree) if d == 0)
    order = []
    while pending:
        u = pending.popleft()
        order.append(u)
        for v in graph[u]:
            degree[v] -= 1
            if degree[v] == 0:
                pending.append(v)
        emit_state(emit, f'取出零入度节点 {u}，删除它的出边。',
                   [f'{i}:入度{d}' for i, d in enumerate(degree)], highlight=[u])
    if len(order) != len(graph):
        raise ValueError('图中有环，无法完成拓扑排序')
    return order


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.count -= 1
        return True


def kruskal(n, edges, emit=None):
    dsu, chosen, total = DSU(n), [], 0
    for weight, a, b in sorted(edges):
        take = dsu.union(a, b)
        if take:
            chosen.append((a, b))
            total += weight
        emit_state(emit, f'边 {a}—{b}，权重 {weight}：'+('选择' if take else '成环，跳过'),
                   [f'总权重 {total}', f'连通分量 {dsu.count}'], chosenEdges=chosen)
    return total, chosen, dsu.count


def quintic_trajectory(distance, duration, steps=40, emit=None):
    if duration <= 0 or steps < 1:
        raise ValueError('总时间和采样步数必须为正')
    result = []
    for i in range(steps + 1):
        tau = i / steps
        position = distance * (10*tau**3 - 15*tau**4 + 6*tau**5)
        velocity = distance / duration * (30*tau**2 - 60*tau**3 + 30*tau**4)
        acceleration = distance / duration**2 * (60*tau - 180*tau**2 + 120*tau**3)
        result.append((duration*tau, position, velocity, acceleration))
        emit_state(emit, f't={duration*tau:.2f}，s={position:.3f}，v={velocity:.3f}，a={acceleration:.3f}',
                   samples=result)
    return result


class DStarLite:
    """Four-connected undirected grid; lazy deletion of obsolete queue entries."""
    def __init__(self, grid, start, goal):
        if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
            raise ValueError('地图必须是非空矩形')
        if any(not (0 <= r < len(grid) and 0 <= c < len(grid[0])) for r,c in (start,goal)):
            raise ValueError('起终点不能超出地图')
        if any(grid[r][c] == '#' for r,c in (start,goal)):
            raise ValueError('起终点必须可通行')
        self.grid = [list(row) for row in grid]
        self.start, self.goal, self.last = start, goal, start
        self.km = 0
        self.g, self.rhs = {}, {goal: 0}
        self.heap, self.pending = [], {}
        self.push(goal)

    def h(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def value(self, table, u):
        return table.get(u, math.inf)

    def key(self, u):
        best = min(self.value(self.g, u), self.value(self.rhs, u))
        return best+self.h(self.start, u)+self.km, best

    def neighbors(self, u):
        r, c = u
        return [(a, b) for a, b in ((r-1,c),(r+1,c),(r,c-1),(r,c+1))
                if 0 <= a < len(self.grid) and 0 <= b < len(self.grid[0])]

    def cost(self, u, v):
        return math.inf if self.grid[u[0]][u[1]] == '#' or self.grid[v[0]][v[1]] == '#' else 1

    def push(self, u):
        key = self.key(u)
        self.pending[u] = key
        heapq.heappush(self.heap, (key, u))

    def top(self):
        while self.heap and self.pending.get(self.heap[0][1]) != self.heap[0][0]:
            heapq.heappop(self.heap)
        return self.heap[0][0] if self.heap else (math.inf, math.inf)

    def update(self, u):
        if u != self.goal:
            self.rhs[u] = min((self.cost(u,v)+self.value(self.g,v)
                               for v in self.neighbors(u)), default=math.inf)
        self.pending.pop(u, None)
        if self.value(self.g,u) != self.value(self.rhs,u):
            self.push(u)

    def scores(self):
        return {f'{r},{c}': dict(w=1, g=self.value(self.g,(r,c)), rhs=self.value(self.rhs,(r,c)),
                                known=(r,c) in self.g or (r,c) in self.rhs)
                for r in range(len(self.grid)) for c in range(len(self.grid[0]))
                if self.grid[r][c] != '#'}

    def repair(self, emit=None):
        while self.top() < self.key(self.start) or self.value(self.rhs,self.start) != self.value(self.g,self.start):
            old, u = heapq.heappop(self.heap)
            self.pending.pop(u, None)
            if old < self.key(u):
                self.push(u)
            elif self.value(self.g,u) > self.value(self.rhs,u):
                self.g[u] = self.value(self.rhs,u)
                for p in self.neighbors(u):
                    self.update(p)
            else:
                self.g[u] = math.inf
                self.update(u)
                for p in self.neighbors(u):
                    self.update(p)
            emit_state(emit, f'修复 {u}：g={self.value(self.g,u)}，rhs={self.value(self.rhs,u)}；km={self.km}',
                       [f'队列 {len(self.pending)}'], grid=[''.join(r) for r in self.grid],
                       start=self.start, goal=self.goal, current=u,
                       visited=[v for v,g in self.g.items() if math.isfinite(g)],
                       scores=self.scores(), scoreKind='dstar')

    def change(self, cell, blocked):
        if cell in (self.start, self.goal):
            raise ValueError('不能把当前位置或目标设为障碍')
        self.grid[cell[0]][cell[1]] = '#' if blocked else '.'
        for u in [cell]+self.neighbors(cell):
            self.update(u)

    def move(self, start):
        self.km += self.h(self.last, start)
        self.start = self.last = start

    def path(self):
        if not math.isfinite(self.value(self.rhs,self.start)):
            return []
        route, seen = [self.start], {self.start}
        while route[-1] != self.goal:
            u = route[-1]
            v = min(self.neighbors(u), key=lambda v: self.cost(u,v)+self.value(self.g,v))
            if v in seen or not math.isfinite(self.cost(u,v)+self.value(self.g,v)):
                return []
            route.append(v)
            seen.add(v)
        return route


def collision_free(a, b, obstacles):
    """Segment against closed axis-aligned rectangles using slab intersection."""
    for left, bottom, right, top in obstacles:
        low, high = 0.0, 1.0
        for p, delta, lo, hi in ((a[0],b[0]-a[0],left,right),
                                  (a[1],b[1]-a[1],bottom,top)):
            if abs(delta) < 1e-12:
                if not lo <= p <= hi:
                    low, high = 1.0, 0.0
                    break
            else:
                t1, t2 = sorted(((lo-p)/delta, (hi-p)/delta))
                low, high = max(low,t1), min(high,t2)
        if low <= high:
            return False
    return True


def rrt(start, goal, obstacles, iterations=180, seed=7, star=False, emit=None):
    if iterations < 0:
        raise ValueError('采样次数不能为负')
    if not collision_free(start,start,obstacles) or not collision_free(goal,goal,obstacles):
        raise ValueError('起点或终点位于障碍内')
    rng, points, parents, costs = random.Random(seed), [start], [-1], [0.0]
    step, goal_candidates, route = 0.9, [], []
    for iteration in range(iterations):
        sample = goal if rng.random() < 0.12 else (rng.uniform(0,10),rng.uniform(0,10))
        near = min(range(len(points)), key=lambda j: math.dist(points[j],sample))
        distance = math.dist(points[near],sample)
        if distance < 1e-10:
            continue
        scale = min(1.0,step/distance)
        new = tuple(points[near][k]+scale*(sample[k]-points[near][k]) for k in (0,1))
        if not collision_free(points[near],new,obstacles):
            continue
        radius = min(2.5, 9.0*math.sqrt(math.log(len(points)+1)/(len(points)+1)))
        neighbors = [j for j,p in enumerate(points) if math.dist(p,new) <= radius] if star else [near]
        feasible = [j for j in set(neighbors+[near]) if collision_free(points[j],new,obstacles)]
        parent = min(feasible,key=lambda j: costs[j]+math.dist(points[j],new))
        index = len(points)
        points.append(new)
        parents.append(parent)
        costs.append(costs[parent]+math.dist(points[parent],new))
        rewired = []
        if star:
            for j in neighbors:
                candidate = costs[index]+math.dist(new,points[j])
                if j and candidate+1e-9 < costs[j] and collision_free(new,points[j],obstacles):
                    parents[j] = index
                    costs[j] = candidate
                    rewired.append(j)
                    # Propagate updated cost through every descendant.
                    queue = deque([j])
                    while queue:
                        p = queue.popleft()
                        for child in range(1,len(points)):
                            if parents[child] == p:
                                costs[child] = costs[p]+math.dist(points[p],points[child])
                                queue.append(child)
        if math.dist(new,goal) <= step and collision_free(new,goal,obstacles):
            goal_candidates.append(index)
        route = []
        if goal_candidates:
            p = min(goal_candidates,key=lambda j:costs[j]+math.dist(points[j],goal))
            route = [goal]
            while p != -1:
                route.append(points[p])
                p = parents[p]
            route.reverse()
        emit_state(emit, f'采样 {iteration+1}：新增节点 {index}；重连 {rewired}；'+('已有可行路径' if route else '尚未连到目标'),
                   [f'树节点 {len(points)}',f'半径 {radius:.2f}'],
                   scene=dict(points=points,parents=parents,obstacles=obstacles,start=start,goal=goal,
                              sample=sample,route=route))
    return points, parents, costs, route if iterations else []
