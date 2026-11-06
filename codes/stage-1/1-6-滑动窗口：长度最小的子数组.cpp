// 滑动窗口：长度最小的子数组
// 学习重点：先把右边的一天加入当前区间，直到积分够用。
// 够用时记录长度，并试着去掉最左边的一天。
// 不够后继续向右扩张，每个边界都只往前走。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <algorithm>  // 排序、取最值、合并或反转等标准算法

using namespace std;

// 正整数条件下移动窗口，寻找达到目标和的最短连续区间。
int minSubArrayLen(int target, vector<int>& nums) {
    // 用当前合法窗口更新最短长度；长度包含左右两端。
    int left = 0, sum = 0, best = (int)nums.size() + 1;
    for (int right = 0; right < (int)nums.size(); ++right) {
        sum += nums[right];
        // 只要仍达到目标就继续收缩；只缩一次可能漏掉更短答案。
        while (sum >= target) {
            // 用当前合法窗口更新最短长度；长度包含左右两端。
            best = min(best, right - left + 1);
            // 左端离开窗口前先扣掉它的积分，再移动左边界。
            sum -= nums[left];
            ++left;
        }
    }
    // 用当前合法窗口更新最短长度；长度包含左右两端。
    return best == (int)nums.size() + 1 ? 0 : best;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{2,3,1,2,4,3,1,2,5};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << minSubArrayLen(7,a) << "\n";
    return 0;
}
