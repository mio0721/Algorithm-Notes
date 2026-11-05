def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

nums = [0, 0, 1, 1, 2, 2, 3, 3, 4]
k = remove_duplicates(nums)
print("长度:", k, "有效元素:", nums[:k])
