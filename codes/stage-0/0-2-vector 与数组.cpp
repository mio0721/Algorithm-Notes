// vector 与数组
// 学习重点：把数据按顺序放进容器。
// 用下标定位，用循环逐个查看。
// 追加或删除后重新确认长度和有效下标。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <cstddef>  // 标准无符号大小类型

using namespace std;

// 建立一个小型动态数组并返回，演示追加元素与按下标遍历。
vector<int> makeValues() {
    // 保存一串按位置编号的数据，编号从0开始。
    vector<int> nums;
    // 把新读数追加到末尾；容量不足时可能搬迁底层存储。
    nums.push_back(4);
    nums.push_back(7);
    return nums;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 保存一串按位置编号的数据，编号从0开始。
    auto nums = makeValues();
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (size_t i = 0; i < nums.size(); ++i) cout << i << ": " << nums[i] << "\n";
    return 0;
}
