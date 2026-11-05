#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < (int)nums.size(); ++fast) {
        if (nums[fast] != nums[slow]) {
            ++slow;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}

int main() {
    vector<int> a{0,0,1,1,2,2,3,3,4};
    int k=removeDuplicates(a);
    cout << "长度: " << k << "，有效元素: ";
    for(int i=0;i<k;++i) cout << a[i] << " ";
    cout << "\n";
    return 0;
}
