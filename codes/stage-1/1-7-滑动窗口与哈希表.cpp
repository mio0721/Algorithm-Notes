#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

int main() {
    string s = "abcabcbbd";
    unordered_map<char, int> last;
    int left = 0, best = 0;

    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
        char ch = s[right];
        if (last.count(ch)) {
            // 左边界不能后退。
            left = max(left, last[ch] + 1);
        }
        last[ch] = right;
        best = max(best, right - left + 1);
    }

    cout << best << endl;
    return 0;
}
