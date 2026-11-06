// 图的基本结构
// 学习重点：列出要描述的对象，给每个对象一个节点。
// 根据实际规则添加连接，并明确方向。
// 有距离、时间等成本时，把它记录为边权。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表

using namespace std;

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
struct Edge { int to; int weight; };
// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<Edge>> graph(3);
    // 有向边只表示从当前起点到终点；不自动添加反向通路。
    graph[0].push_back({1,4});
    graph[1].push_back({2,3});
    for (int u=0; u<3; ++u)
        for (const auto& edge : graph[u])
            // 输出计算结果，便于与课程例子或自行推演的答案核对。
            cout << u << " -> " << edge.to << "，权重 " << edge.weight << "\n";
}
