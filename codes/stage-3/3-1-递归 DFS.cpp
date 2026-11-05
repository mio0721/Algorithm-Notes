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

    function<void(int)> dfs = [&](int u) {
        seen[u] = true;
        cout << char('A' + u) << " ";

        for (int v : g[u]) {
            if (!seen[v]) {
                dfs(v);
            }
        }
    };

    dfs(0);
    cout << endl;
    return 0;
}
