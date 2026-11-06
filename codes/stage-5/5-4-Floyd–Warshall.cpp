// Floyd–Warshall
// 学习重点：先填好直接边的距离表。
// 选一个中转点，查看任意起终点经它是否更近。
// 所有中转点都试完，得到任意两点的最短距离。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <limits>  // 整数边界或浮点无穷大
#include <stdexcept>  // 明确报告非法输入

using namespace std;

const long long INF = numeric_limits<long long>::max()/4;
// 逐轮开放中转点，只有两段均可达时才尝试更新距离。
vector<vector<long long>> floyd(vector<vector<long long>> distance) {
    int n = static_cast<int>(distance.size());
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    for (const auto& row : distance) if (static_cast<int>(row.size()) != n) throw invalid_argument("not square");
    // 中转点必须在最外层，表示本轮新允许使用哪个中转点。
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                // 两段都可达时才相加，避免把无穷大标记参与整数运算。
                if (distance[i][k] != INF && distance[k][j] != INF) {
                    distance[i][j] = min(distance[i][j], distance[i][k]+distance[k][j]);
                }
            }
        }
    }
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    for (int i = 0; i < n; ++i) if (distance[i][i] < 0) throw invalid_argument("negative cycle");
    return distance;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<long long>> distance{{0,3,10,INF},{INF,0,4,8},{INF,INF,0,2},{1,INF,INF,0}};
    for (const auto& row : floyd(distance)) {
        for (long long cost : row) {
            // 输出计算结果，便于与课程例子或自行推演的答案核对。
            if (cost == INF) cout << "INF "; else cout << cost << ' ';
        }
        cout << '\n';
    }
}
