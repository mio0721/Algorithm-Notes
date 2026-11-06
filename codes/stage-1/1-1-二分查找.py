# 二分查找
# Python 3；直接运行文件，修改示例数据可继续练习。
# 保留一段仍可能包含目标的位置。

# 在有序数组的闭区间内查找目标，找到返回下标，找不到返回−1。
def search(nums, target):
    left, right = (0, len(nums) - 1)
    # 闭区间只剩一个位置时仍需检查，所以条件包含相等。
    while left <= right:
        # 用左端加一半区间长度求中点，避免直接相加的溢出风险。
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            # 中点已确认太小，连同它一起排除，边界必须真正前进。
            left = mid + 1
        else:
            # 中点已确认太大，后续不再重复检查它。
            right = mid - 1
    return -1
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(search([-5, -1, 0, 3, 5, 9, 12, 16, 20], 9))
