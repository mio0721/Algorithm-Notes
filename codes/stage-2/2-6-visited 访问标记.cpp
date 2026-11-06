// visited 访问标记
// 学习重点：准备一份访问标记。
// 发现一个新节点时，先标记，再加入待处理集合。
// 只继续处理尚未标记的邻居。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> graph{{1,2},{0,2},{0,1}};
    // 访问标记初始为空或全为假，表示还没有发现节点。
    vector<bool> visited(graph.size(), false);
    queue<int> pending;
    // 发现时先标记，避免多个邻居把同一个节点重复入队。
    int start=0; visited[start]=true; pending.push(start);
    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {
        // 读取先进先出的队首，保持发现的层次顺序。
        int u=pending.front(); pending.pop();
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << "访问 " << char('A'+u) << "\n";
        for (int v : graph[u]) if (!visited[v]) {
            // 发现时先标记，避免多个邻居把同一个节点重复入队。
            visited[v]=true; pending.push(v);
        }
    }
}
