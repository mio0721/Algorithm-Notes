#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

vector<int> twoSum(vector<int>& numbers, int target) {
    int left = 0, right = (int)numbers.size() - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) return {left + 1, right + 1};
        if (sum < target) ++left;
        else --right;
    }
    return {}; // 通用写法；原题保证有解
}

int main() {
    vector<int> a{1,2,4,6,9,12,15,19,23};
    for (int i : twoSum(a,17)) cout << i << " ";
    cout << "\n";
    return 0;
}
