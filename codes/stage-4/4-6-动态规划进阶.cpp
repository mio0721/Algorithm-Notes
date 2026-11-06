// 动态规划进阶
// 学习重点：先考虑两份记录很短的前缀。
// 末尾相同，就把这一对字符接在较短问题的结果后面。
// 末尾不同，就分别尝试跳过其中一边的末尾。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <string>  // 字符串存储与操作
#include <algorithm>  // 排序、取最值、合并或反转等标准算法

using namespace std;

// 填公共前缀状态表，再沿最优邻格回溯出一个最长公共子序列。
string lcs(const string& a, const string& b) {
    int m = static_cast<int>(a.size()), n = static_cast<int>(b.size());
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    // 第0行、0列表示空前缀，所以真实字符从下标i−1、j−1读取。
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            dp[i][j] = a[i - 1] == b[j - 1]
                ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    string result;
    while (m > 0 && n > 0) {
        if (a[m - 1] == b[n - 1]) {
            result.push_back(a[--m]);
            --n;
        } else if (dp[m - 1][n] >= dp[m][n - 1]) {
            --m;
        } else {
            --n;
        }
    }
    // 回溯收集的是倒序公共字符，输出前需要反转。
    reverse(result.begin(), result.end());
    return result;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    string result = lcs("ABCBDAB", "BDCABA");
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << result.size() << ' ' << result << '\n';
}
