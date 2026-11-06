// 队列 BFS
// 学习重点：起点先入队，并立即标记。
// 取出最早发现的节点。
// 把它未发现的邻居按顺序加入队尾。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列

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
    // 访问标记初始为空或全为假，表示还没有发现节点。
    vector<bool> seen(g.size(), false);
    queue<int> pending;
    pending.push(0);
    // 入队前标记，一个节点只加入一次。
    seen[0] = true;

    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {
        // 取最早发现的节点，保持逐层扩展顺序。
        int u = pending.front();
        pending.pop();
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << char('A' + u) << " ";

        for (int v : g[u]) {
            if (!seen[v]) {
                // 入队前标记，一个节点只加入一次。
                seen[v] = true;
                pending.push(v);
            }
        }
    }
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << endl;
    return 0;
}
