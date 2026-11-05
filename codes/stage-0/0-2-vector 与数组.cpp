#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

vector<int> makeValues() {
    vector<int> nums;
    nums.push_back(4);
    nums.push_back(7);
    return nums;
}

int main() {
    auto nums = makeValues();
    for (size_t i = 0; i < nums.size(); ++i) cout << i << ": " << nums[i] << "\n";
    return 0;
}
