# 无权图最短路径
# Python 3；直接运行文件，修改示例数据可继续练习。
# 起点距离记为0。

from collections import deque
g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
# 没有前驱的起点用−1标记，回溯到这里就结束。
dist, parent = ([-1] * 10, [-1] * 10)
dist[0], queue = (0, deque([0]))
# 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
while queue:
    # 读取先进先出的队首，保持发现的层次顺序。
    u = queue.popleft()
    for v in g[u]:
        if dist[v] == -1:
            # 第一次发现时保存前驱，最后通过前驱链恢复真实路线。
            dist[v], parent[v] = (dist[u] + 1, u)
            queue.append(v)
if dist[9] == -1:
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('unreachable')
else:
    path, node = ([], 9)
    while node != -1:
        path.append(chr(65 + node))
        # 第一次发现时保存前驱，最后通过前驱链恢复真实路线。
        node = parent[node]
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(path[::-1], 'steps=', dist[9])
