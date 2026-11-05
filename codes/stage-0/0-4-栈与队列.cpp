#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int queueFirst() {
    queue<int> q;
    q.push(4);
    q.push(7);
    if (q.empty()) return -1;
    int value = q.front();
    q.pop();
    return value;
}

int main() {
    cout << "队首: " << queueFirst() << "\n";
    stack<int> s; s.push(4); s.push(7); cout << "栈顶: " << s.top() << "\n";
    return 0;
}
