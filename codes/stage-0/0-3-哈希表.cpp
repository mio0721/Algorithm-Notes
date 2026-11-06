// 哈希表 unordered_map 与 unordered_set
// 学习重点：明确只需要判断存在，还是需要保存编号对应的值。
// 按键查找已有记录。
// 需要时插入新键或更新它的值。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <unordered_map>  // 哈希映射，按键查找记录

using namespace std;

// 从哈希表查询键对应的下标，不存在时返回−1，不修改原表。
int findIndex(const unordered_map<int,int>& mp, int key) {
    // 只查询已有键，不为了检查存在而插入默认记录。
    auto it = mp.find(key);
    if (it == mp.end()) return -1;
    return it->second;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    unordered_map<int,int> mp{{4,0},{7,1}};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << findIndex(mp,4) << " " << findIndex(mp,9) << "\n";
    return 0;
}
