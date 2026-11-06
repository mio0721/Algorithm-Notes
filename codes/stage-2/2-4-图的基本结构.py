# 图的基本结构
# Python 3；直接运行文件，修改示例数据可继续练习。
# 列出要描述的对象，给每个对象一个节点。

graph = [[], [], []]
# 有向边只表示从当前起点到终点；不自动添加反向通路。
graph[0].append((1, 4))
graph[1].append((2, 3))
for start, edges in enumerate(graph):
    for end, weight in edges:
        # 输出计算结果，便于与课程例子或自行推演的答案核对。
        print(f'{start} -> {end}，权重 {weight}')
