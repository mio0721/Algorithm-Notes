# 拓扑排序
# Python 3；直接运行文件，修改示例数据可继续练习。
# 数清每个任务还有几个未完成的前置任务。

from collections import deque

# 持续处理没有剩余前置依赖的任务；处理不完全部任务就报告有向环。
def topological_sort(graph):
    degree = [0] * len(graph)
    for row in graph:
        for v in row:
            degree[v] += 1
    pending = deque((i for i, d in enumerate(degree) if d == 0))
    order = []
    # 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while pending:
        # 读取先进先出的队首，保持发现的层次顺序。
        u = pending.popleft()
        order.append(u)
        for v in graph[u]:
            degree[v] -= 1
            if degree[v] == 0:
                pending.append(v)
    # 未能处理全部顶点意味着存在依赖环，不能把部分顺序当完整答案。
    if len(order) != len(graph):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('图中有环，无法完成拓扑排序')
    return order

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    graph = [[2, 3], [3], [4], [4, 5], [6], [7], [8], [8], [9], []]
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(topological_sort(graph))
    try:
        topological_sort([[1], [0]])
    except ValueError as error:
        print(error)
if __name__ == '__main__':
    main()
