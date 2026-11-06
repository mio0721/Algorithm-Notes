// 无权图最短路径
// 学习重点：起点距离记为0。
// 第一次发现邻居时记录距离与它从哪里来。
// 到终点后沿前驱回到起点，再翻转路线。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列
#include <algorithm>  // 排序、取最值、合并或反转等标准算法

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> g = {
        {1, 2},
        {0, 3, 4},
        {0, 5, 6},
        {1, 7},
        {1, 8, 5},
        {2, 4},
        {2, 9},
        {3},
        {4, 9},
        {6, 8}
    };
    // 没有前驱的起点用−1标记，回溯到这里就结束。
    vector<int> parent(g.size(), -1);
    vector<int> distance(g.size(), -1);
    queue<int> pending;
    const int start = 0, goal = 9;
    pending.push(start);
    distance[start] = 0;

    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {
        // 读取先进先出的队首，保持发现的层次顺序。
        int u = pending.front();
        pending.pop();

        for (int v : g[u]) {
            if (distance[v] == -1) {
                distance[v] = distance[u] + 1;
                // 第一次发现时保存前驱，最后通过前驱链恢复真实路线。
                parent[v] = u;
                pending.push(v);
            }
        }
    }

    if (distance[goal] == -1) {
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << "unreachable" << endl;
        return 0;
    }

    vector<int> path;
    // 第一次发现时保存前驱，最后通过前驱链恢复真实路线。
    for (int u = goal; u != -1; u = parent[u]) {
        path.push_back(u);
    }
    // 回溯顺序是终点到起点，反转后才是执行方向。
    reverse(path.begin(), path.end());

    for (int u : path) {
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << char('A' + u) << " ";
    }
    cout << "steps=" << distance[goal] << endl;
    return 0;
}
