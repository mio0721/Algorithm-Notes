#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int minSubArrayLen(int target, vector<int>& nums) {
    int left = 0, sum = 0, best = (int)nums.size() + 1;
    for (int right = 0; right < (int)nums.size(); ++right) {
        sum += nums[right];
        while (sum >= target) {
            best = min(best, right - left + 1);
            sum -= nums[left];
            ++left;
        }
    }
    return best == (int)nums.size() + 1 ? 0 : best;
}

int main() {
    vector<int> a{2,3,1,2,4,3,1,2,5};
    cout << minSubArrayLen(7,a) << "\n";
    return 0;
}
