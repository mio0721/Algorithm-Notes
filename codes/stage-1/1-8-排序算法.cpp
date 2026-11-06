// 排序算法
// 学习重点：左边保留已经有序的部分。
// 取出右边下一个值，把比它大的左侧元素向后挪。
// 空出的地方放回这个值，再处理下一张。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<int> a{9, 3, 7, 1, 8, 2, 6, 4, 5};

    for (int i = 1; i < static_cast<int>(a.size()); ++i) {
        // 先保存待插入值，防止移动数组时覆盖它。
        int value = a[i];
        int j = i - 1;


        // 把比待插入值大的元素向后挪；相等时不挪，保留稳定性。
        while (j >= 0 && a[j] > value) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = value;
    }

    for (int value : a) {
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << value << " ";
    }
    cout << endl;
    return 0;
}
