// A*
// 学习重点：记录已经走到当前格花了多少。
// 估计从这里到目标至少还要多少。
// 优先尝试两者合起来较小的位置，碰到更便宜路线就更新。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <string>  // 字符串存储与操作
#include <queue>  // 先进先出队列或优先队列
#include <map>  // 有序映射，按节点保存状态
#include <functional>  // 递归函数包装或堆比较器
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <tuple>  // 多字段状态与字典序比较
#include <cmath>  // 距离、幂、平方根或数值判断
#include <stdexcept>  // 明确报告非法输入

using namespace std;

using Cell = pair<int, int>;
// 按已走代价加剩余下界选择扩展顺序，终点有效出队后恢复路径。
vector<Cell> astar(const vector<string>& grid, Cell start, Cell goal, bool useHeuristic = true) {
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (grid.empty() || grid[0].empty()) throw invalid_argument("empty map");
    int rows = static_cast<int>(grid.size()), cols = static_cast<int>(grid[0].size());
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    for (const auto& row : grid) if (static_cast<int>(row.size()) != cols) throw invalid_argument("ragged map");
    auto valid = [&](Cell p) {
        return p.first >= 0 && p.first < rows && p.second >= 0 && p.second < cols;
    };
    if (!valid(start) || !valid(goal)) throw invalid_argument("endpoint outside map");
    if (grid[start.first][start.second] == '#' || grid[goal.first][goal.second] == '#') return {};
    // 四邻域单位步长使用曼哈顿距离作为剩余代价下界；h=0退化为一致代价搜索。
    auto heuristic = [&](Cell p) {
        return useHeuristic ? abs(p.first-goal.first)+abs(p.second-goal.second) : 0;
    };
    map<Cell,int> distance;
    map<Cell,Cell> parent;
    using Entry = tuple<int,int,Cell>;
    priority_queue<Entry,vector<Entry>,greater<Entry>> heap;
    distance[start] = 0;
    heap.push({heuristic(start),0,start});
    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!heap.empty()) {
        auto [estimate,cost,u] = heap.top();
        // 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
        heap.pop();
        if (distance[u] != cost) continue;
        if (u == goal) {
            vector<Cell> route{u};
            while (u != start) {
                u = parent.at(u);
                route.push_back(u);
            }
            // 把反向收集的数据恢复为实际输出顺序。
            reverse(route.begin(),route.end());
            return route;
        }
        for (Cell delta : vector<Cell>{{-1,0},{1,0},{0,-1},{0,1}}) {
            Cell v{u.first+delta.first,u.second+delta.second};
            if (!valid(v) || grid[v.first][v.second] == '#') continue;
            if (!distance.count(v) || cost+1 < distance[v]) {
                distance[v] = cost+1;
                // 只在路线改善时更新前驱，恢复时才有完整可行的父链。
                parent[v] = u;
                // 四邻域单位步长使用曼哈顿距离作为剩余代价下界；h=0退化为一致代价搜索。
                heap.push({cost+1+heuristic(v),cost+1,v});
            }
        }
    }
    return {};
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<string> grid{".........", ".###.###.", "...#.....", "...#.###.", ".........", "..###...."};
    auto route = astar(grid,{0,0},{5,8});
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (route.empty()) { cout << "unreachable\n"; return 0; }
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "steps=" << route.size()-1 << '\n';
    for (auto [r,c] : route) if (grid[r][c] != '#') grid[r][c] = '*';
    for (const auto& row : grid) cout << row << '\n';
}
