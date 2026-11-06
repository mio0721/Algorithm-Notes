# RRT
# Python 3；直接运行文件，修改示例数据可继续练习。
# 随机采一个点。

import math
import random

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
        # 线段参数与矩形在两个坐标轴的区间有公共部分，就发生碰撞。
        if low <= high:
            return False
    return True

# 随机采样并向最近节点扩展，只保留整段无碰撞的连接；返回采样树与找到的路径。
def rrt(start, goal, obstacles, iterations=180, seed=7):
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
        # 单次扩展最多走一个步长，不直接跳到远处样本。
        scale = min(1.0, step / distance)
        new = tuple((points[near][k] + scale * (sample[k] - points[near][k]) for k in (0, 1)))
        if not collision_free(points[near], new, obstacles):
            continue
        parent = near
        index = len(points)
        points.append(new)
        parents.append(parent)
        costs.append(costs[parent] + math.dist(points[parent], new))
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
    points, parents, costs, route = rrt((1, 1), (9, 9), [(3, 2, 6, 7)], 250, 7)
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('nodes:', len(points))
    print('route:', route or 'not found within budget')
    print('length:', sum((math.dist(a, b) for a, b in zip(route, route[1:]))))
if __name__ == '__main__':
    main()
