#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int main() {
    vector<vector<int>> graph(8);
    auto addEdge = [&](int a, int b) { graph[a].push_back(b); graph[b].push_back(a); };
    for (auto edge : vector<pair<int,int>>{{0,1},{0,2},{1,3},{1,4},{2,5},{2,6},{6,7},{4,7}})
        addEdge(edge.first, edge.second);
    for (int i=0; i<8; ++i) {
        cout << i << ": ";
        for (int neighbor : graph[i]) cout << neighbor << " ";
        cout << "\n";
    }
}
