# 算法与时间复杂度
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先数一次核心动作，例如比较一次书名。

def linear_search(nums, target):
    # 这一轮核心操作执行多少次，取决于循环变量怎样变化；观察次数而不只看运行秒数。
    for index, value in enumerate(nums):
        if value == target:
            return index
    return -1
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(linear_search([2, 4, 6, 8], 6))
