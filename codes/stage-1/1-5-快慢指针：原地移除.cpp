#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int removeElement(vector<int>& nums, int val) {
    int slow = 0;
    for (int fast = 0; fast < (int)nums.size(); ++fast) {
        if (nums[fast] != val) {
            nums[slow] = nums[fast];
            ++slow;
        }
    }
    return slow;
}

int main() {
    vector<int> a{3,2,2,3,4,3,5,2,3};
    int k=removeElement(a,3);
    cout << "长度: " << k << "，有效元素: ";
    for(int i=0;i<k;++i) cout << a[i] << " ";
    cout << "\n";
    return 0;
}
