// 快慢指针：原地移除
// 学习重点：扫描指针查看每个原始值。
// 不等于待删除值时，复制到下一个可写位置。
// 写入指针走了多远，就是保留了多少个值。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 保留不等于指定值的元素，返回覆盖写入后的有效长度。
int removeElement(vector<int>& nums, int val) {
    int slow = 0;
    for (int fast = 0; fast < (int)nums.size(); ++fast) {
        // 只有不等于待移除值的元素才保留，重复的有效值仍需保留。
        if (nums[fast] != val) {
            // 把有效值覆盖到下一个写入位置，不在遍历中反复erase。
            nums[slow] = nums[fast];
            ++slow;
        }
    }
    return slow;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{3,2,2,3,4,3,5,2,3};
    int k=removeElement(a,3);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "长度: " << k << "，有效元素: ";
    for(int i=0;i<k;++i) cout << a[i] << " ";
    cout << "\n";
    return 0;
}
