// 二分边界与插入位置
// 学习重点：把目标左边应出现的“小于目标”部分不断确定下来。
// 遇到不小于目标的值，就把它保留为可能的分界线。
// 没有候选位置时，当前边界就是插入位置。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 寻找第一个不小于目标的位置；允许返回数组长度作为末尾插入位置。
int searchInsert(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size();
    // 本课使用左闭右开区间；左右相等时已经没有候选元素。
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < target) left = mid + 1;
        // 当前值不小于目标，保留中点作为潜在插入边界。
        else right = mid;
    }
    // 返回边界，允许等于长度；不要直接读取这个位置的元素。
    return left;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{1,3,5,6,8,10,12,15,18};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << searchInsert(a,7) << "\n";
    return 0;
}
