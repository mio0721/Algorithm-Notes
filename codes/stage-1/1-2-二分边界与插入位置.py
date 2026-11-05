def search_insert(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

print(search_insert([1, 3, 5, 6, 8, 10, 12, 15, 18], 7))
