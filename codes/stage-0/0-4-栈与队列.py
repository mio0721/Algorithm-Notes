# 栈与队列
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先根据任务选择“后来先出”或“先来先出”。

from collections import deque
stack = [4, 7]
queue = deque([4, 7])
# 栈的最近加入项先离开；取出前必须确认非空。
print('栈顶:', stack.pop())
# 队列的最早加入项先离开。
print('队首:', queue.popleft())
