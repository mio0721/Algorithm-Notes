# 滑动窗口：长度最小的子数组
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先把右边的一天加入当前区间，直到积分够用。

def min_subarray_len(target, nums):
    left = total = 0
    # 用当前合法窗口更新最短长度；长度包含左右两端。
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        # 只要仍达到目标就继续收缩；只缩一次可能漏掉更短答案。
        while total >= target:
            # 用当前合法窗口更新最短长度；长度包含左右两端。
            best = min(best, right - left + 1)
            # 左端离开窗口前先扣掉它的积分，再移动左边界。
            total -= nums[left]
            left += 1
    # 用当前合法窗口更新最短长度；长度包含左右两端。
    return 0 if best == len(nums) + 1 else best
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(min_subarray_len(7, [2, 3, 1, 2, 4, 3, 1, 2, 5]))
