// 相向双指针
// 学习重点：左手指最小候选，右手指最大候选。
// 两数相加偏小，就让左手换一个更大的数。
// 偏大就让右手换小一点；相等就找到答案。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 在有序数组上用相向指针寻找两个不同位置，使其和值等于目标。
vector<int> twoSum(vector<int>& numbers, int target) {
    int left = 0, right = (int)numbers.size() - 1;
    // 左右必须是不同位置，不能把同一个元素使用两次。
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) return {left + 1, right + 1};
        // 和偏小，排除当前最小候选；有序性保证不会漏掉正确配对。
        if (sum < target) ++left;
        // 和偏大，排除当前最大候选。
        else --right;
    }
    return {};
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{1,2,4,6,9,12,15,19,23};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int i : twoSum(a,17)) cout << i << " ";
    cout << "\n";
    return 0;
}
