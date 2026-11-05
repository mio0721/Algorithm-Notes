#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int sum(int n) {
    cout << "进入 " << n << "\n";
    if (n == 0) return 0;
    int smaller = sum(n - 1);
    cout << "返回 " << n << "\n";
    return n + smaller;
}

int main() {
    int result=sum(2);
    cout << "结果: " << result << "\n";
    return 0;
}
