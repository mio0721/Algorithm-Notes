#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

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
    vector<bool> onPath(g.size(), false);
    vector<int> path;
    const int goal = 9;

    function<void(int)> dfs = [&](int u) {
        onPath[u] = true;
        path.push_back(u);

        if (u == goal) {
            for (int v : path) {
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

        // 撤销当前选择，让其他路径可以使用这个节点。
        path.pop_back();
        onPath[u] = false;
    };

    dfs(0);
    return 0;
}
