// 滑动窗口与哈希表
// 学习重点：右边每读到一个字符，检查它上次出现在哪里。
// 若重复位置还在窗口里，就把左边界跳到它后面。
// 保存每个字符的最新位置，并更新最长长度。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <string>  // 字符串存储与操作
#include <unordered_map>  // 哈希映射，按键查找记录
#include <algorithm>  // 排序、取最值、合并或反转等标准算法

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    string s = "abcabcbbd";
    unordered_map<char, int> last;
    int left = 0, best = 0;

    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
        char ch = s[right];
        if (last.count(ch)) {

            // 左边界只能前进，不能被窗口外的旧出现位置拉回。
            left = max(left, last[ch] + 1);
        }
        // 每轮更新字符最后一次出现的位置，供下一次重复判断。
        last[ch] = right;
        best = max(best, right - left + 1);
    }

    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << best << endl;
    return 0;
}
