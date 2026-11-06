# 树的层序遍历
# Python 3；直接运行文件，修改示例数据可继续练习。
# 当前队列里保存本层节点。

from collections import deque
children = [[1, 2], [3, 4], [5, 6], [7], [8], [], [9], [], [], []]
queue = deque([0])
# 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
while queue:
    level = []
    # 每层先保存队列当前长度，只处理这一层原有节点。
    for _ in range(len(queue)):
        # 读取先进先出的队首，保持发现的层次顺序。
        node = queue.popleft()
        level.append(node + 1)
        queue.extend(children[node])
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(level)
