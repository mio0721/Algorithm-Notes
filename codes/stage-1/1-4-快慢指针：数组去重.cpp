// 快慢指针：有序数组去重
// 学习重点：一个指针扫描原数据，另一个指针标记已保留结果的末端。
// 扫描到与上一个已保留值不同的数时，写入下一个有效位置。
// 最后只看有效前缀。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 把有序数组中的不同值写入有效前缀，并返回有效元素数量。
int removeDuplicates(vector<int>& nums) {
    // 先处理空输入，避免读取第一个元素。
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < (int)nums.size(); ++fast) {
        if (nums[fast] != nums[slow]) {
            ++slow;
            // 发现新值时才写入有效前缀，末尾旧内容无需清空。
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{0,0,1,1,2,2,3,3,4};
    int k=removeDuplicates(a);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "长度: " << k << "，有效元素: ";
    for(int i=0;i<k;++i) cout << a[i] << " ";
    cout << "\n";
    return 0;
}
