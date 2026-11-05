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
    vector<string> grid{"....", ".##.", "...."};
    int rows = static_cast<int>(grid.size());
    int cols = static_cast<int>(grid[0].size());
    vector<vector<bool>> seen(rows, vector<bool>(cols, false));
    int dr[]{1, -1, 0, 0};
    int dc[]{0, 0, 1, -1};

    function<bool(int, int)> dfs = [&](int r, int c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) {
            return false;
        }
        if (grid[r][c] == '#' || seen[r][c]) {
            return false;
        }

        seen[r][c] = true;
        if (r == rows - 1 && c == cols - 1) {
            return true;
        }

        for (int k = 0; k < 4; ++k) {
            if (dfs(r + dr[k], c + dc[k])) {
                return true;
            }
        }
        return false;
    };

    cout << (dfs(0, 0) ? "reachable" : "unreachable") << endl;
    return 0;
}
