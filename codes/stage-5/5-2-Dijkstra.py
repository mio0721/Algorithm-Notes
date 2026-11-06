# Dijkstra
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先记起点路程为0，其他点暂时不知道。

import math
import heapq

# 非负权条件下优先处理当前最小有效距离，返回距离表与前驱表。
def dijkstra(graph, start):
    if any((weight < 0 for row in graph for _, weight in row)):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('Dijkstra 不支持负边权')
    # 没有前驱的起点用−1标记，回溯到这里就结束。
    distance, parent = ([math.inf] * len(graph), [-1] * len(graph))
    distance[start] = 0
    pending = [(0, start)]
    settled = set()
    # 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while pending:
        # 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
        cost, u = heapq.heappop(pending)
        # 旧堆记录可能还在，但距离已经改善；过期记录直接跳过。
        if cost != distance[u]:
            continue
        settled.add(u)
        for v, weight in graph[u]:
            candidate = cost + weight
            # 只有严格更短的路线才松弛，避免零权边反复制造重复记录。
            if candidate < distance[v]:
                distance[v], parent[v] = (candidate, u)
                # 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
                heapq.heappush(pending, (candidate, v))
    return (distance, parent)

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    graph = [[] for _ in range(10)]
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 4, 5), (3, 5, 3), (4, 5, 1), (5, 6, 2), (6, 7, 1), (7, 8, 2), (8, 9, 1)]:
        graph[u].append((v, w))
    distance, parent = dijkstra(graph, 0)
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('distance:', distance)
    route, u = ([], 9)
    if math.isfinite(distance[u]):
        while u != -1:
            route.append(u)
            u = parent[u]
    print('route:', route[::-1])
if __name__ == '__main__':
    main()
