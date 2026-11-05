#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int smallest() {
    priority_queue<int, vector<int>, greater<int>> pq;
    pq.push(5);
    pq.push(2);
    int x = pq.top();
    pq.pop();
    return x;
}

int main() {
    cout << "最小值: " << smallest() << "\n";
    return 0;
}
