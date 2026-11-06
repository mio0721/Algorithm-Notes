// 递归 DFS
// 学习重点：进入当前位置并标记已发现。
// 找一个没走过的邻居，继续深入。
// 没有可走邻居就返回上一层，尝试其他分支。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <functional>  // 递归函数包装或堆比较器

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

    function<void(int)> dfs = [&](int u) {
        // 进入节点立即标记，环上的边就不会造成无限递归。
        seen[u] = true;
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << char('A' + u) << " ";

        for (int v : g[u]) {
            // 只沿尚未发现的邻居继续深入。
            if (!seen[v]) {
                dfs(v);
            }
        }
    };

    dfs(0);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << endl;
    return 0;
}
