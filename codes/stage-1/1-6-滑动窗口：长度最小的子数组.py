def min_subarray_len(target, nums):
    left = total = 0
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == len(nums) + 1 else best

print(min_subarray_len(7, [2, 3, 1, 2, 4, 3, 1, 2, 5]))
