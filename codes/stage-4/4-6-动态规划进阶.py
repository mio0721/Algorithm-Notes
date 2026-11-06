# 动态规划进阶
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先考虑两份记录很短的前缀。

# 填公共前缀状态表，再沿最优邻格回溯出一个最长公共子序列。
def lcs(first, second):
    m, n = (len(first), len(second))
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # 第0行、0列表示空前缀，所以真实字符从下标i−1、j−1读取。
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    path, i, j = ([], m, n)
    while i and j:
        if first[i - 1] == second[j - 1]:
            path.append(first[i - 1])
            i, j = (i - 1, j - 1)
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    # 回溯收集的是倒序公共字符，输出前需要反转。
    return (dp[m][n], ''.join(reversed(path)))

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(lcs('ABCBDAB', 'BDCABA'))
if __name__ == '__main__':
    main()
