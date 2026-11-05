#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}

int main() {
    cout << "sum(3) = " << sum(3) << "\n";
    return 0;
}
