// 二分查找
// 学习重点：保留一段仍可能包含目标的位置。
// 查看这段中间的数。
// 相等就结束；否则排除不可能的一半，再重复。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 在有序数组的闭区间内查找目标，找到返回下标，找不到返回−1。
int search(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    // 闭区间只剩一个位置时仍需检查，所以条件包含相等。
    while (left <= right) {
        // 用左端加一半区间长度求中点，避免直接相加的溢出风险。
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        // 中点已确认太小，连同它一起排除，边界必须真正前进。
        if (nums[mid] < target) left = mid + 1;
        // 中点已确认太大，后续不再重复检查它。
        else right = mid - 1;
    }
    return -1;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{-5,-1,0,3,5,9,12,16,20};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << search(a,9) << "\n";
    return 0;
}
