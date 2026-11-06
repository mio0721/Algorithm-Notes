// 动态规划基础
// 学习重点：先算出最小几个台阶的走法数。
// 每个更大的问题，只从已经算好的较小问题得到答案。
// 把算过的结果存下来，避免反复重算。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <stdexcept>  // 明确报告非法输入

using namespace std;

// 保存到达每级台阶的方案数；输入上限用于防止long long溢出。
long long climbStairs(int n) {
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    if (n < 0 || n > 90) throw invalid_argument("n must be in [0,90]");
    vector<long long> dp(n + 1);
    // 到0级时什么也不做，是一种完整方案。
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        // 按最后一步来自前一级或前两级分类，不会重复计数。
        dp[i] = dp[i - 1];
        if (i >= 2) dp[i] += dp[i - 2];
    }
    return dp[n];
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int n : {0, 1, 5, 9}) cout << n << ": " << climbStairs(n) << '\n';
}
