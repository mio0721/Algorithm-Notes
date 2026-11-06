// 图的遍历与连通性
// 学习重点：从一个未访问点发起完整搜索。
// 这次找到的所有点归到同一组。
// 继续找下一个未访问点，直到全部处理完。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <utility>  // 二元组、交换或移动对象

using namespace std;

// 从每个尚未归类的节点发起搜索，输出无向图的各个连通分量。
vector<vector<int>> components(const vector<vector<int>>& graph) {
    // 访问标记初始为空或全为假，表示还没有发现节点。
    vector<bool> visited(graph.size(), false);
    vector<vector<int>> groups;
    for (int start = 0; start < static_cast<int>(graph.size()); ++start) {
        // 已经归类的节点无需重复发起搜索。
        if (visited[start]) continue;
        // 为本次搜索新建一个连通分量，孤立点也会形成一组。
        groups.push_back({});
        vector<int> stack{start};
        visited[start] = true;
        // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
        while (!stack.empty()) {
            int u = stack.back();
            stack.pop_back();
            // 为本次搜索新建一个连通分量，孤立点也会形成一组。
            groups.back().push_back(u);
            for (int v : graph[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    stack.push_back(v);
                }
            }
        }
    }
    return groups;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> graph(10);
    for (auto [u, v] : vector<pair<int,int>>{{0,1},{1,2},{2,3},{4,5},{5,6},{7,8}}) {
        graph[u].push_back(v);
        graph[v].push_back(u);
    }
    auto result = components(graph);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "components=" << result.size() << '\n';
    for (const auto& group : result) {
        for (int u : group) cout << char('A' + u) << ' ';
        cout << '\n';
    }
}
