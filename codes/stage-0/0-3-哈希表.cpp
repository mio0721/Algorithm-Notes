#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int findIndex(const unordered_map<int,int>& mp, int key) {
    auto it = mp.find(key);
    if (it == mp.end()) return -1;
    return it->second;
}

int main() {
    unordered_map<int,int> mp{{4,0},{7,1}};
    cout << findIndex(mp,4) << " " << findIndex(mp,9) << "\n";
    return 0;
}
