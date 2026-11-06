// 图的存储：邻接表与邻接矩阵
// 学习重点：先确定节点编号。
// 枚举邻居频繁时，使用每个点的一份邻居列表。
// 需要频繁判断特定两点是否直接相连时，考虑二维矩阵。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <utility>  // 二元组、交换或移动对象

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> graph(8);
    // 无向边需要在两个节点的邻居表中各存一次。
    auto addEdge = [&](int a, int b) { graph[a].push_back(b); graph[b].push_back(a); };
    for (auto edge : vector<pair<int,int>>{{0,1},{0,2},{1,3},{1,4},{2,5},{2,6},{6,7},{4,7}})
        addEdge(edge.first, edge.second);
    for (int i=0; i<8; ++i) {
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << i << ": ";
        for (int neighbor : graph[i]) cout << neighbor << " ";
        cout << "\n";
    }
}
