// 非递归 DFS
// 学习重点：把起点加入栈并标记。
// 取出栈顶，处理它。
// 把未发现的邻居压栈，直到栈为空。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <stack>  // 后进先出的显式栈

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
    stack<int> pending;
    pending.push(0);
    // 压栈时标记，避免同一节点重复加入待处理栈。
    seen[0] = true;

    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {
        int u = pending.top();
        pending.pop();
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << char('A' + u) << " ";


        // 栈后进先出；想先访问的邻居应后压入。
        for (auto it = g[u].rbegin(); it != g[u].rend(); ++it) {
            int v = *it;
            if (!seen[v]) {
                // 压栈时标记，避免同一节点重复加入待处理栈。
                seen[v] = true;
                pending.push(v);
            }
        }
    }
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << endl;
    return 0;
}
