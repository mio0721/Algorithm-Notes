#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int main() {
    vector<vector<int>> graph{{1,2},{0,2},{0,1}};
    vector<bool> visited(graph.size(), false);
    queue<int> pending;
    int start=0; visited[start]=true; pending.push(start);
    while (!pending.empty()) {
        int u=pending.front(); pending.pop();
        cout << "访问 " << char('A'+u) << "\n";
        for (int v : graph[u]) if (!visited[v]) {
            visited[v]=true; pending.push(v);
        }
    }
}
