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
    vector<int> a{9, 3, 7, 1, 8, 2, 6, 4, 5};

    for (int i = 1; i < static_cast<int>(a.size()); ++i) {
        int value = a[i];
        int j = i - 1;

        // 大于待插入值的元素依次右移。
        while (j >= 0 && a[j] > value) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = value;
    }

    for (int value : a) {
        cout << value << " ";
    }
    cout << endl;
    return 0;
}
