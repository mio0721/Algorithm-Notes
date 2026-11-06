// 贪心算法
// 学习重点：按结束时间从早到晚排活动。
// 能接在上一个活动后面就选择。
// 冲突的活动跳过，继续看下一个。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <tuple>  // 多字段状态与字典序比较
#include <limits>  // 整数边界或浮点无穷大
#include <stdexcept>  // 明确报告非法输入

using namespace std;

// 按结束时间从早到晚考虑活动，返回互不重叠的最大数量活动列表。
vector<pair<int, int>> selectIntervals(vector<pair<int, int>> intervals) {
    for (auto [start, end] : intervals) {
        // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        if (end < start) throw invalid_argument("end before start");
    }
    // 按结束时间而非开始时间、时长排序。
    sort(intervals.begin(), intervals.end(), [](auto a, auto b) {
        return tie(a.second, a.first) < tie(b.second, b.first);
    });
    vector<pair<int, int>> chosen;
    // 保存上一个已选择任务的结束时刻，后面的任务不能与它冲突。
    long long lastEnd = numeric_limits<long long>::lowest();
    for (auto [start, end] : intervals) {
        if (start >= lastEnd) {
            chosen.push_back({start, end});
            lastEnd = end;
        }
    }
    return chosen;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    auto result = selectIntervals({{1,4}, {3,5}, {0,6}, {5,7}, {3,9},
                                   {5,9}, {6,10}, {8,11}, {8,9}});
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (auto [start, end] : result) cout << '[' << start << ',' << end << ")\n";
    cout << "count=" << result.size() << '\n';
}
