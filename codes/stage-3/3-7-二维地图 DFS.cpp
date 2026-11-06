// 二维地图 DFS
// 学习重点：从起点进入格子并标记。
// 依次检查上下左右：先看是否越界，再看是否障碍或已访问。
// 能进入就继续深入，否则回到上一格尝试。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <string>  // 字符串存储与操作
#include <functional>  // 递归函数包装或堆比较器

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<string> grid{"....", ".##.", "...."};
    int rows = static_cast<int>(grid.size());
    int cols = static_cast<int>(grid[0].size());
    // 访问标记初始为空或全为假，表示还没有发现节点。
    vector<vector<bool>> seen(rows, vector<bool>(cols, false));
    int dr[]{1, -1, 0, 0};
    int dc[]{0, 0, 1, -1};

    function<bool(int, int)> dfs = [&](int r, int c) {
        // 先检查坐标合法，再检查障碍与访问状态，防止越界。
        if (r < 0 || r >= rows || c < 0 || c >= cols) {
            return false;
        }
        if (grid[r][c] == '#' || seen[r][c]) {
            return false;
        }

        seen[r][c] = true;
        if (r == rows - 1 && c == cols - 1) {
            // 找到一条路线即返回成功；这不保证它是最短路线。
            return true;
        }

        for (int k = 0; k < 4; ++k) {
            if (dfs(r + dr[k], c + dc[k])) {
                // 找到一条路线即返回成功；这不保证它是最短路线。
                return true;
            }
        }
        return false;
    };

    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << (dfs(0, 0) ? "reachable" : "unreachable") << endl;
    return 0;
}
