# 快慢指针：原地移除
# Python 3；直接运行文件，修改示例数据可继续练习。
# 扫描指针查看每个原始值。

def remove_element(nums, value):
    slow = 0
    for fast in range(len(nums)):
        # 只有不等于待移除值的元素才保留，重复的有效值仍需保留。
        if nums[fast] != value:
            # 把有效值覆盖到下一个写入位置，不在遍历中反复erase。
            nums[slow] = nums[fast]
            slow += 1
    return slow
nums = [3, 2, 2, 3, 4, 3, 5, 2, 3]
k = remove_element(nums, 3)
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print('长度:', k, '有效元素:', nums[:k])
