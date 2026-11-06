# RRT*
# Python 3；直接运行文件，修改示例数据可继续练习。
# 新点出现后，在附近可连接的节点中选总成本最低的父节点。

import math
import random
from collections import deque

# 用线段参数区间检测闭矩形碰撞；接触障碍边界也视为碰撞。
def collision_free(a, b, obstacles):
    """通过线段参数区间求交检测闭矩形障碍；边界接触也算碰撞。"""
    for left, bottom, right, top in obstacles:
        low, high = (0.0, 1.0)
        for p, delta, lo, hi in ((a[0], b[0] - a[0], left, right), (a[1], b[1] - a[1], bottom, top)):
            if abs(delta) < 1e-12:
                if not lo <= p <= hi:
                    low, high = (1.0, 0.0)
                    break
            else:
                t1, t2 = sorted(((lo - p) / delta, (hi - p) / delta))
                low, high = (max(low, t1), min(high, t2))
        if low <= high:
            return False
    return True

# 在连续空间采样、扩展与检测碰撞；启用star时增加邻域选父和重连。
def rrt(start, goal, obstacles, iterations=180, seed=7, star=False):
    if iterations < 0:
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('采样次数不能为负')
    if not collision_free(start, start, obstacles) or not collision_free(goal, goal, obstacles):
        raise ValueError('起点或终点位于障碍内')
    # 没有前驱的起点用−1标记，回溯到这里就结束。
    rng, points, parents, costs = (random.Random(seed), [start], [-1], [0.0])
    step, goal_candidates, route = (0.9, [], [])
    for iteration in range(iterations):
        sample = goal if rng.random() < 0.12 else (rng.uniform(0, 10), rng.uniform(0, 10))
        near = min(range(len(points)), key=lambda j: math.dist(points[j], sample))
        distance = math.dist(points[near], sample)
        if distance < 1e-10:
            continue
        scale = min(1.0, step / distance)
        new = tuple((points[near][k] + scale * (sample[k] - points[near][k]) for k in (0, 1)))
        if not collision_free(points[near], new, obstacles):
            continue
        # 二维邻域半径随有效样本数收缩，演示常数不直接等于理论保证。
        radius = min(2.5, 9.0 * math.sqrt(math.log(len(points) + 1) / (len(points) + 1)))
        neighbors = [j for j, p in enumerate(points) if math.dist(p, new) <= radius] if star else [near]
        feasible = [j for j in set(neighbors + [near]) if collision_free(points[j], new, obstacles)]
        parent = min(feasible, key=lambda j: costs[j] + math.dist(points[j], new))
        index = len(points)
        points.append(new)
        parents.append(parent)
        costs.append(costs[parent] + math.dist(points[parent], new))
        rewired = []
        if star:
            for j in neighbors:
                candidate = costs[index] + math.dist(new, points[j])
                if j and candidate + 1e-09 < costs[j] and collision_free(new, points[j], obstacles):
                    # 只有经新节点严格更便宜且线段无碰撞，才重连旧节点。
                    parents[j] = index
                    costs[j] = candidate
                    rewired.append(j)
                    queue = deque([j])
                    # 把重连造成的成本变化传给全部后代，不能只改一个父指针。
                    while queue:
                        # 读取先进先出的队首，保持发现的层次顺序。
                        p = queue.popleft()
                        for child in range(1, len(points)):
                            if parents[child] == p:
                                costs[child] = costs[p] + math.dist(points[p], points[child])
                                queue.append(child)
        if math.dist(new, goal) <= step and collision_free(new, goal, obstacles):
            goal_candidates.append(index)
        route = []
        if goal_candidates:
            p = min(goal_candidates, key=lambda j: costs[j] + math.dist(points[j], goal))
            route = [goal]
            while p != -1:
                route.append(points[p])
                p = parents[p]
            # 把反向收集的数据恢复为实际输出顺序。
            route.reverse()
    return (points, parents, costs, route if iterations else [])

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    points, parents, costs, route = rrt((1, 1), (9, 9), [(3, 2, 6, 7)], 250, 7, True)
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('nodes:', len(points))
    print('route:', route or 'not found within budget')
    print('length:', sum((math.dist(a, b) for a, b in zip(route, route[1:]))))
if __name__ == '__main__':
    main()
