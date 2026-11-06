// 分治算法
// 学习重点：把大数组拆成两小段。
// 小段也用同样办法，直到只剩一个数。
// 把两段有序结果按大小合并。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <functional>  // 递归函数包装或堆比较器
#include <algorithm>  // 排序、取最值、合并或反转等标准算法

using namespace std;

// 用一份共享辅助数组合并左右有序子段，原地更新原数组内容。
void mergeSort(vector<int>& nums) {
    vector<int> buffer(nums.size());
    function<void(int, int)> sortRange = [&](int left, int right) {
        if (right - left <= 1) return;
        int middle = left + (right - left) / 2;
        sortRange(left, middle);
        sortRange(middle, right);
        int a = left, b = middle, output = left;
        while (a < middle && b < right) {
            // 相等时优先取左边，保持相等元素的相对顺序。
            buffer[output++] = nums[a] <= nums[b] ? nums[a++] : nums[b++];
        }
        while (a < middle) buffer[output++] = nums[a++];
        while (b < right) buffer[output++] = nums[b++];
        // 合并完成后写回对应区间，左右子问题的有序结果才能变成整段有序。
        copy(buffer.begin() + left, buffer.begin() + right, nums.begin() + left);
    };
    sortRange(0, static_cast<int>(nums.size()));
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> nums{8, 3, 7, 1, 9, 2, 6, 4, 5};
    mergeSort(nums);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int value : nums) cout << value << ' ';
    cout << '\n';
}
