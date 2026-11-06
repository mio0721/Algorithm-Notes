# 图的存储：邻接表与邻接矩阵
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先确定节点编号。

graph = [[] for _ in range(8)]
for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7), (4, 7)]:
    # 无向边需要在两个节点的邻居表中各存一次。
    graph[a].append(b)
    graph[b].append(a)
for node, neighbors in enumerate(graph):
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(f'{node}: {neighbors}')
