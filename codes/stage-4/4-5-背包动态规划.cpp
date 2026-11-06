// 背包动态规划
// 学习重点：一件件考虑装备，比较带与不带。
// 为不同剩余容量保存最好结果。
// 处理同一件装备时，不能重复拿它。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <stdexcept>  // 明确报告非法输入
#include <cstddef>  // 标准无符号大小类型

using namespace std;

// 每件物品最多使用一次，对各容量比较不选与选一次的最大价值。
long long knapsack(const vector<int>& weights, const vector<int>& values, int capacity) {
    if (weights.size() != values.size() || capacity < 0) {
        // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        throw invalid_argument("invalid dimensions");
    }
    vector<long long> dp(capacity + 1, 0);
    for (size_t i = 0; i < weights.size(); ++i) {
        if (weights[i] <= 0) throw invalid_argument("weights must be positive");

        // 容量必须倒序，确保当前物品最多使用一次。
        for (int c = capacity; c >= weights[i]; --c) {
            // 比较不选当前物品与选一次后的总价值，保留较好结果。
            dp[c] = max(dp[c], dp[c - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << knapsack({2, 3, 4, 5}, {3, 4, 5, 8}, 9) << '\n';
    cout << knapsack({2}, {3}, 4) << '\n';
}
