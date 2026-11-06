// 回溯算法
// 学习重点：保存当前已经选出的装备。
// 尝试再选一件后面的装备，继续探索。
// 试完后把这件撤销，回到原来的选择再试别的。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <functional>  // 递归函数包装或堆比较器

using namespace std;

// 枚举当前路径和所有后续扩展，返回每个合法子集的一份独立副本。
vector<vector<int>> subsets(const vector<int>& nums) {
    vector<vector<int>> answer;
    vector<int> path;
    function<void(int)> visit = [&](int start) {
        // 立即保存当前选择的副本，包含什么也不选的空集。
        answer.push_back(path);
        for (int i = start; i < static_cast<int>(nums.size()); ++i) {
            path.push_back(nums[i]);
            // 只从后续下标选择，避免同一个组合换顺序后重复输出。
            visit(i + 1);
            // 撤销本轮选择，恢复进入分支前的状态。
            path.pop_back();
        }
    };
    visit(0);
    return answer;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    for (const auto& subset : subsets({1, 2, 3, 4})) {
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << "[ ";
        for (int value : subset) cout << value << ' ';
        cout << "]\n";
    }
}
