def remove_element(nums, value):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != value:
            nums[slow] = nums[fast]
            slow += 1
    return slow

nums = [3, 2, 2, 3, 4, 3, 5, 2, 3]
k = remove_element(nums, 3)
print("长度:", k, "有效元素:", nums[:k])
