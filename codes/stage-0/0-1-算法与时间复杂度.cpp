// 算法与时间复杂度
// 学习重点：先数一次核心动作，例如比较一次书名。
// 观察数据变多后，动作次数是保持不变、翻倍，还是增长得更快。
// 用增长类型描述方法，最后再认识它的复杂度符号。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

int linearSearch(const vector<int>& nums, int target) {
    // 这一轮核心操作执行多少次，取决于循环变量怎样变化；观察次数而不只看运行秒数。
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (nums[i] == target) return i;
    }
    return -1;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << linearSearch(vector<int>{2, 4, 6, 8}, 6) << "\n";
    return 0;
}
