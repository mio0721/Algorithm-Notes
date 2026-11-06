// 二维地图 BFS 与对比
// 学习重点：起点距离设为0并入队。
// 每次出队，发现邻格时记录距离和前驱。
// 终点可达就回溯路线；否则明确返回无路。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <string>  // 字符串存储与操作
#include <queue>  // 先进先出队列或优先队列
#include <utility>  // 二元组、交换或移动对象

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
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

    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {
        // 读取先进先出的队首，保持发现的层次顺序。
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
            // 四邻域每走一步代价相同，距离比父格多1。
            distance[nr][nc] = distance[r][c] + 1;
            pending.push({nr, nc});
        }
    }

    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "steps=" << distance[rows - 1][cols - 1] << endl;
    return 0;
}
