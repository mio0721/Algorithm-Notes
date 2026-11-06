// DFS 与回溯
// 学习重点：进入节点时把它加入当前路线。
// 到达目标就保存路线副本。
// 返回时撤销本层路线与路径标记。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <functional>  // 递归函数包装或堆比较器

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> g = {
        {1, 2},
        {3, 4},
        {5, 6},
        {7},
        {8, 5},
        {},
        {9},
        {},
        {9},
        {}
    };
    // 返回上一层时恢复现场，让兄弟分支可以独立探索。
    vector<bool> onPath(g.size(), false);
    vector<int> path;
    const int goal = 9;

    function<void(int)> dfs = [&](int u) {
        onPath[u] = true;
        // 把当前位置加入当前路线，不代表永久禁止其他路径使用它。
        path.push_back(u);

        if (u == goal) {
            for (int v : path) {
                // 输出计算结果，便于与课程例子或自行推演的答案核对。
                cout << char('A' + v) << " ";
            }
            cout << endl;
        } else {
            for (int v : g[u]) {
                if (!onPath[v]) {
                    dfs(v);
                }
            }
        }


        // 返回上一层时恢复现场，让兄弟分支可以独立探索。
        path.pop_back();
        onPath[u] = false;
    };

    dfs(0);
    return 0;
}
