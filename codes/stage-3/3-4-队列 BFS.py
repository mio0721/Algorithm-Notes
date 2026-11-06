# 队列 BFS
# Python 3；直接运行文件，修改示例数据可继续练习。
# 起点先入队，并立即标记。

from collections import deque
g = [[1, 2], [0, 3, 4], [0, 5, 6], [1, 7], [1, 8, 5], [2, 4], [2, 9], [3], [4, 9], [6, 8]]
seen, queue = ({0}, deque([0]))
# 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
while queue:
    # 取最早发现的节点，保持逐层扩展顺序。
    u = queue.popleft()
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(chr(65 + u), end=' ')
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            queue.append(v)
print()
