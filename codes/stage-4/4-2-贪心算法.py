# 贪心算法
# Python 3；直接运行文件，修改示例数据可继续练习。
# 按结束时间从早到晚排活动。

import math

# 按结束时间从早到晚考虑活动，返回互不重叠的最大数量活动列表。
def select_intervals(intervals):
    if any((end < start for start, end in intervals)):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('区间终点不能小于起点')
    # 保存上一个已选择任务的结束时刻，后面的任务不能与它冲突。
    chosen, end_time = ([], -math.inf)
    # 按结束时间而非开始时间、时长排序。
    for start, end in sorted(intervals, key=lambda pair: (pair[1], pair[0])):
        # 保存上一个已选择任务的结束时刻，后面的任务不能与它冲突。
        take = start >= end_time
        if take:
            chosen.append((start, end))
            end_time = end
    return chosen

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(select_intervals([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 9)]))
if __name__ == '__main__':
    main()
