// 动态重规划与 D* Lite
// 学习重点：先从目标反向维护“走到目标还要多少代价”。
// 地图变化后，找出当前记录与新的一步估计不一致的格子。
// 把这些差异按优先级传播修复，直到当前位置可据此提取路线。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <string>  // 字符串存储与操作
#include <queue>  // 先进先出队列或优先队列
#include <map>  // 有序映射，按节点保存状态
#include <set>  // 有序集合或路径内去重
#include <functional>  // 递归函数包装或堆比较器
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <limits>  // 整数边界或浮点无穷大
#include <cmath>  // 距离、幂、平方根或数值判断
#include <stdexcept>  // 明确报告非法输入

using namespace std;

using Cell = pair<int,int>;
using Key = pair<double,double>;
const double INF = numeric_limits<double>::infinity();

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
class DStarLite {
    vector<string> grid;
    Cell start, goal, last;
    double km = 0;
    map<Cell,double> g, rhs;
    map<Cell,Key> pending;
    using Entry = pair<Key,Cell>;
    priority_queue<Entry,vector<Entry>,greater<Entry>> heap;

    // 读取状态表；尚未建立记录的顶点统一视为无穷大。
    double value(const map<Cell,double>& table, Cell u) const {
        auto it = table.find(u);
        return it == table.end() ? INF : it->second;
    }
    double heuristic(Cell a, Cell b) const {
        return abs(a.first-b.first)+abs(a.second-b.second);
    }
    // 计算两个字段组成的关键字，先比较第一项，相等时再比较第二项。
    Key key(Cell u) const {
        double best = min(value(g,u),value(rhs,u));
        return {best+heuristic(start,u)+km,best};
    }
    // 枚举地图内的四个相邻格；是否能穿过障碍由边代价函数进一步决定。
    vector<Cell> neighbors(Cell u) const {
        vector<Cell> result;
        for (auto [dr,dc] : vector<Cell>{{-1,0},{1,0},{0,-1},{0,1}}) {
            Cell v{u.first+dr,u.second+dc};
            if (v.first >= 0 && v.first < static_cast<int>(grid.size()) &&
                v.second >= 0 && v.second < static_cast<int>(grid[0].size())) result.push_back(v);
        }
        return result;
    }
    // 任一端点是障碍时边代价为无穷大，否则四邻域一步代价为1。
    double cost(Cell a, Cell b) const {
        return grid[a.first][a.second] == '#' || grid[b.first][b.second] == '#' ? INF : 1;
    }
    // 登记顶点当前有效关键字并压入最小堆，旧副本暂时保留。
    void push(Cell u) {
        pending[u] = key(u);
        // 加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。
        heap.push({pending[u],u});
    }
    // 在查看堆顶前丢弃过期副本，只返回当前有效的最小关键字。
    Key top() {
        // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
        while (!heap.empty()) {
            auto [k,u] = heap.top();
            auto it = pending.find(u);
            if (it != pending.end() && it->second == k) return k;
            // 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
            heap.pop();
        }
        return {INF,INF};
    }
    // 重新计算一跳前瞻代价；只有g与rhs不一致的顶点才需要进入修复队列。
    void update(Cell u) {
        if (u != goal) {
            rhs[u] = INF;
            for (Cell v : neighbors(u)) rhs[u] = min(rhs[u],cost(u,v)+value(g,v));
        }
        // 删除当前有效队列登记；堆中的历史副本由top惰性丢弃。
        pending.erase(u);
        if (value(g,u) != value(rhs,u)) push(u);
    }
public:
    DStarLite(vector<string> map, Cell s, Cell t) : grid(move(map)),start(s),goal(t),last(s) {
        // 先处理空容器或无结果情况，避免访问不存在的元素。
        if (grid.empty() || grid[0].empty()) throw invalid_argument("empty map");
        // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        for (const auto& row : grid) if (row.size() != grid[0].size()) throw invalid_argument("ragged map");
        for (Cell u : {start,goal}) {
            if (u.first < 0 || u.first >= static_cast<int>(grid.size()) ||
                u.second < 0 || u.second >= static_cast<int>(grid[0].size()) || grid[u.first][u.second] == '#') {
                throw invalid_argument("invalid endpoint");
            }
        }
        // 目标的一跳前瞻代价固定为0，其余未建立的状态视为无穷大。
        rhs[goal] = 0;
        push(goal);
    }
    // 传播不一致状态，直到当前位置一致，且队列没有更小关键字需要处理。
    void repair() {
        while (top() < key(start) || value(rhs,start) != value(g,start)) {
            auto [old,u] = heap.top();
            // 处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。
            heap.pop();
            // 删除当前有效队列登记；堆中的历史副本由top惰性丢弃。
            pending.erase(u);
            // 起点移动后关键字可能变大，先重新计算并按新键入队。
            if (old < key(u)) {
                push(u);
            } else if (value(g,u) > value(rhs,u)) {
                g[u] = value(rhs,u);
                for (Cell p : neighbors(u)) update(p);
            } else {
                // 旧代价失效时先设为无穷大，再重新传播，不直接把坏状态当作有效答案。
                g[u] = INF;
                // 重新检查当前顶点是否一致；不一致才进入修复队列。
                update(u);
                for (Cell p : neighbors(u)) update(p);
            }
        }
    }
    // 修改一个格子的占据状态，并更新它及相邻格受影响的边代价。
    void change(Cell u, bool blocked) {
        // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        if (u == start || u == goal) throw invalid_argument("cannot block endpoint");
        grid.at(u.first).at(u.second) = blocked ? '#' : '.';
        // 重新检查当前顶点是否一致；不一致才进入修复队列。
        update(u);
        for (Cell p : neighbors(u)) update(p);
    }
    // 起点移动后维护关键字偏移km，保留并复用原有搜索数据。
    void moveStart(Cell s) {
        // 移动起点时累加启发式偏移，复用原队列和搜索状态。
        km += heuristic(last,s);
        start = last = s;
    }
    // 沿边代价加后继g最小的方向提取路线，检测无路与异常循环。
    vector<Cell> path() const {
        if (!isfinite(value(rhs,start))) return {};
        vector<Cell> route{start};
        set<Cell> seen{start};
        while (route.back() != goal) {
            Cell u = route.back(), best{-1,-1};
            double distance = INF;
            for (Cell v : neighbors(u)) {
                double candidate = cost(u,v)+value(g,v);
                if (candidate < distance) { distance = candidate; best = v; }
            }
            if (!isfinite(distance) || seen.count(best)) return {};
            route.push_back(best);
            seen.insert(best);
        }
        return route;
    }
};

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    DStarLite planner({".........",".###.###.","...#.....","...#.###.",".........","..###...."},{0,0},{5,8});
    planner.repair();
    auto before = planner.path();
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "initial steps=" << before.size()-1 << '\n';
    Cell changed = before.at(before.size()/2);
    planner.change(changed,true);
    planner.repair();
    auto after = planner.path();
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (after.empty()) cout << "unreachable\n";
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    else cout << "repaired steps=" << after.size()-1 << '\n';
    planner.change(changed,false);
    planner.repair();
    cout << "restored steps=" << planner.path().size()-1 << '\n';
}
