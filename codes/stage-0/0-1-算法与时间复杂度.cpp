#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int linearSearch(const vector<int>& nums, int target) {
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (nums[i] == target) return i;
    }
    return -1;
}

int main() {
    cout << linearSearch(vector<int>{2, 4, 6, 8}, 6) << "\n";
    return 0;
}
