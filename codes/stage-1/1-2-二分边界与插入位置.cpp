#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int searchInsert(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < target) left = mid + 1;
        else right = mid;
    }
    return left;
}

int main() {
    vector<int> a{1,3,5,6,8,10,12,15,18};
    cout << searchInsert(a,7) << "\n";
    return 0;
}
