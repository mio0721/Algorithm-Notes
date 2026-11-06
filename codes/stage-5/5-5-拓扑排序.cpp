// 拓扑排序
// 学习重点：数清每个任务还有几个未完成的前置任务。
// 把没有前置阻碍的任务加入队列。
// 做完一个任务，减少它后续任务的剩余依赖。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列
#include <stdexcept>  // 明确报告非法输入

using namespace std;

// 持续处理没有剩余前置依赖的任务；处理不完全部任务就报告有向环。
vector<int> topologicalSort(const vector<vector<int>>& graph) {
    vector<int> indegree(graph.size());
    for (const auto& edges : graph) for (int v : edges) ++indegree[v];
    queue<int> ready;
    for (int u = 0; u < static_cast<int>(graph.size()); ++u) if (!indegree[u]) ready.push(u);
    vector<int> order;
    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!ready.empty()) {
        // 读取先进先出的队首，保持发现的层次顺序。
        int u = ready.front();
        ready.pop();
        order.push_back(u);
        // 完成当前任务后，后继少一个未满足依赖；恰好减到0才入队。
        for (int v : graph[u]) if (--indegree[v] == 0) ready.push(v);
    }
    // 未能处理全部顶点意味着存在依赖环，不能把部分顺序当完整答案。
    if (order.size() != graph.size()) throw invalid_argument("dependency cycle");
    return order;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> graph{{2,3},{3},{4},{4,5},{6},{7},{8},{8},{9},{}};
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    for (int u : topologicalSort(graph)) cout << char('A'+u) << ' ';
    cout << '\n';
    try {
        topologicalSort({{1},{0}});
    } catch (const invalid_argument& error) {
        cout << error.what() << '\n';
    }
}
