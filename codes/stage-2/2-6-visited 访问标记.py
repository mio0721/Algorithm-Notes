# visited 访问标记
# Python 3；直接运行文件，修改示例数据可继续练习。
# 准备一份访问标记。

from collections import deque
graph = [[1, 2], [0, 2], [0, 1]]
visited = [False] * len(graph)
pending = deque([0])
# 发现时先标记，避免多个邻居把同一个节点重复入队。
visited[0] = True
# 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
while pending:
    # 读取先进先出的队首，保持发现的层次顺序。
    node = pending.popleft()
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('访问', chr(ord('A') + node))
    for neighbor in graph[node]:
        if not visited[neighbor]:
            # 发现时先标记，避免多个邻居把同一个节点重复入队。
            visited[neighbor] = True
            pending.append(neighbor)
