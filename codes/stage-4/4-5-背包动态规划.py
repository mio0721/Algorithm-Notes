# 背包动态规划
# Python 3；直接运行文件，修改示例数据可继续练习。
# 一件件考虑装备，比较带与不带。

# 每件物品最多使用一次，对各容量比较不选与选一次的最大价值。
def knapsack(weights, values, capacity):
    if len(weights) != len(values) or capacity < 0 or any((w <= 0 for w in weights)):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('重量必须为正，容量非负，重量与价值数量一致')
    dp = [0] * (capacity + 1)
    for item, (weight, value) in enumerate(zip(weights, values)):
        # 容量必须倒序，确保当前物品最多使用一次。
        for room in range(capacity, weight - 1, -1):
            old = dp[room]
            # 比较不选当前物品与选一次后的总价值，保留较好结果。
            dp[room] = max(dp[room], dp[room - weight] + value)
    return dp[capacity]

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(knapsack([2, 3, 4, 5], [3, 4, 5, 8], 9))
    print(knapsack([2], [3], 4))
if __name__ == '__main__':
    main()
