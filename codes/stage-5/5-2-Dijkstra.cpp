// Dijkstra
// 学习重点：先记起点路程为0，其他点暂时不知道。
// 总是先处理当前已知路程最小的点。
// 沿它的边尝试更新邻居的更便宜路线。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列
#include <functional>  // 递归函数包装或堆比较器
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <tuple>  // 多字段状态与字典序比较
#include <limits>  // 整数边界或浮点无穷大
#include <stdexcept>  // 明确报告非法输入

using namespace std;

using WeightedGraph = vector<vector<pair<int, int>>>;
const long long INF = numeric_limits<long long>::max() / 4;

// 非负权条件下优先处理当前最小有效距离，返回距离表与前驱表。
pair<vector<long long>, vector<int>> dijkstra(const WeightedGraph& graph, int start) {
    for (const auto& edges : graph) {
        for (auto [v, weight] : edges) {
            // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
            if (weight < 0) throw invalid_argument("negative edge");
        }
    }
    vector<long long> distance(graph.size(), INF);
    // 没有前驱的起点用−1标记，回溯到这里就结束。
    vector<int> parent(graph.size(), -1);
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> heap;
    distance.at(start) = 0;
    // 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
    heap.push({0, start});
    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!heap.empty()) {
        auto [cost, u] = heap.top();
        // 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
        heap.pop();
        // 旧堆记录可能还在，但距离已经改善；过期记录直接跳过。
        if (cost != distance[u]) continue;
        for (auto [v, weight] : graph[u]) {
            // 只有严格更短的路线才松弛，避免零权边反复制造重复记录。
            if (cost + weight < distance[v]) {
                distance[v] = cost + weight;
                parent[v] = u;
                // 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
                heap.push({distance[v], v});
            }
        }
    }
    return {distance, parent};
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    WeightedGraph graph(10);
    for (auto [u,v,w] : vector<tuple<int,int,int>>{
            {0,1,4},{0,2,1},{2,1,2},{1,3,1},{2,4,5},{3,5,3},
            {4,5,1},{5,6,2},{6,7,1},{7,8,2},{8,9,1}}) graph[u].push_back({v,w});
    auto [distance, parent] = dijkstra(graph, 0);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int u = 0; u < 10; ++u) cout << char('A'+u) << ": " << distance[u] << '\n';
    vector<int> route;
    if (distance[9] != INF) {
        for (int u = 9; u != -1; u = parent[u]) route.push_back(u);
        // 把反向收集的数据恢复为实际输出顺序。
        reverse(route.begin(), route.end());
    }
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int u : route) cout << char('A'+u) << ' ';
    cout << '\n';
}
