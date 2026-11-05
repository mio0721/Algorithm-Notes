#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

struct Edge { int to; int weight; };
int main() {
    vector<vector<Edge>> graph(3);
    graph[0].push_back({1,4});
    graph[1].push_back({2,3});
    for (int u=0; u<3; ++u)
        for (const auto& edge : graph[u])
            cout << u << " -> " << edge.to << "，权重 " << edge.weight << "\n";
}
