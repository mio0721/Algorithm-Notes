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
    vector<vector<int>> children = {
        {1, 2},
        {3, 4},
        {5, 6},
        {7},
        {8},
        {},
        {9},
        {},
        {},
        {}
    };
    queue<int> pending;
    pending.push(0);

    while (!pending.empty()) {
        // 先保存本层长度，避免把下一层混入当前层。
        int count = static_cast<int>(pending.size());
        for (int i = 0; i < count; ++i) {
            int u = pending.front();
            pending.pop();
            cout << u + 1 << " ";

            for (int v : children[u]) {
                pending.push(v);
            }
        }
        cout << endl;
    }
    return 0;
}
