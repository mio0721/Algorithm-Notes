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
    vector<bool> seen(g.size(), false);
    stack<int> pending;
    pending.push(0);
    seen[0] = true;

    while (!pending.empty()) {
        int u = pending.top();
        pending.pop();
        cout << char('A' + u) << " ";

        // 倒序压栈，使编号较小的邻居先出栈。
        for (auto it = g[u].rbegin(); it != g[u].rend(); ++it) {
            int v = *it;
            if (!seen[v]) {
                seen[v] = true;
                pending.push(v);
            }
        }
    }
    cout << endl;
    return 0;
}
