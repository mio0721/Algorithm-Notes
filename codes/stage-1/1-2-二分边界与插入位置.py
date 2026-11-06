# 二分边界与插入位置
# Python 3；直接运行文件，修改示例数据可继续练习。
# 把目标左边应出现的“小于目标”部分不断确定下来。

def search_insert(nums, target):
    left, right = (0, len(nums))
    # 本课使用左闭右开区间；左右相等时已经没有候选元素。
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            # 当前值不小于目标，保留中点作为潜在插入边界。
            right = mid
    # 返回边界，允许等于长度；不要直接读取这个位置的元素。
    return left
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(search_insert([1, 3, 5, 6, 8, 10, 12, 15, 18], 7))
