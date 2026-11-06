# 相向双指针
# Python 3；直接运行文件，修改示例数据可继续练习。
# 左手指最小候选，右手指最大候选。

def two_sum(nums, target):
    left, right = (0, len(nums) - 1)
    # 左右必须是不同位置，不能把同一个元素使用两次。
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            # 和偏小，排除当前最小候选；有序性保证不会漏掉正确配对。
            left += 1
        else:
            # 和偏大，排除当前最大候选。
            right -= 1
    return []
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(two_sum([1, 2, 4, 6, 9, 12, 15, 19, 23], 17))
