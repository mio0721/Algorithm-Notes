def linear_search(nums, target):
    for index, value in enumerate(nums):
        if value == target:
            return index
    return -1

print(linear_search([2, 4, 6, 8], 6))
