# 图的遍历与连通性
# Python 3；直接运行文件，修改示例数据可继续练习。
# 从一个未访问点发起完整搜索。

# 从每个尚未归类的节点发起搜索，输出无向图的各个连通分量。
def components(graph):
    # 访问标记初始为空或全为假，表示还没有发现节点。
    seen, groups = (set(), [])
    for start in range(len(graph)):
        # 已经归类的节点无需重复发起搜索。
        if start in seen:
            continue
        seen.add(start)
        pending, group = ([start], [])
        # 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
        while pending:
            u = pending.pop()
            group.append(u)
            # 把反向收集的数据恢复为实际输出顺序。
            for v in reversed(graph[u]):
                if v not in seen:
                    seen.add(v)
                    pending.append(v)
        # 为本次搜索新建一个连通分量，孤立点也会形成一组。
        groups.append(group)
    return groups

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    graph = [[] for _ in range(10)]
    for u, v in [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (7, 8)]:
        graph[u].append(v)
        graph[v].append(u)
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(components(graph))
if __name__ == '__main__':
    main()
