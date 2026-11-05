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
    vector<int> parent(g.size(), -1);
    vector<int> distance(g.size(), -1);
    queue<int> pending;
    const int start = 0, goal = 9;
    pending.push(start);
    distance[start] = 0;

    while (!pending.empty()) {
        int u = pending.front();
        pending.pop();

        for (int v : g[u]) {
            if (distance[v] == -1) {
                distance[v] = distance[u] + 1;
                parent[v] = u;
                pending.push(v);
            }
        }
    }

    if (distance[goal] == -1) {
        cout << "unreachable" << endl;
        return 0;
    }

    vector<int> path;
    for (int u = goal; u != -1; u = parent[u]) {
        path.push_back(u);
    }
    reverse(path.begin(), path.end());

    for (int u : path) {
        cout << char('A' + u) << " ";
    }
    cout << "steps=" << distance[goal] << endl;
    return 0;
}
