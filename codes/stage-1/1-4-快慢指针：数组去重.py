# 快慢指针：有序数组去重
# Python 3；直接运行文件，修改示例数据可继续练习。
# 一个指针扫描原数据，另一个指针标记已保留结果的末端。

def remove_duplicates(nums):
    # 先处理空输入，避免读取第一个元素。
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            # 发现新值时才写入有效前缀，末尾旧内容无需清空。
            nums[slow] = nums[fast]
    return slow + 1
nums = [0, 0, 1, 1, 2, 2, 3, 3, 4]
k = remove_duplicates(nums)
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print('长度:', k, '有效元素:', nums[:k])
