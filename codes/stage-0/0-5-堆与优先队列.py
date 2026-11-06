# 堆与优先队列
# Python 3；直接运行文件，修改示例数据可继续练习。
# 把任务和优先级一起加入堆。

import heapq
heap = []
# 最小堆先处理较小代价；C++的比较器方向与默认大根堆不同。
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
# 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
print('最小值:', heapq.heappop(heap))
