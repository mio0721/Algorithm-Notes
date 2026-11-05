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
    vector<vector<int>> distance(rows, vector<int>(cols, -1));
    queue<pair<int, int>> pending;
    int dr[]{1, -1, 0, 0};
    int dc[]{0, 0, 1, -1};

    if (grid[0][0] != '#') {
        pending.push({0, 0});
        distance[0][0] = 0;
    }

    while (!pending.empty()) {
        auto [r, c] = pending.front();
        pending.pop();

        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k];
            int nc = c + dc[k];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                continue;
            }
            if (grid[nr][nc] == '#' || distance[nr][nc] != -1) {
                continue;
            }
            distance[nr][nc] = distance[r][c] + 1;
            pending.push({nr, nc});
        }
    }

    cout << "steps=" << distance[rows - 1][cols - 1] << endl;
    return 0;
}
