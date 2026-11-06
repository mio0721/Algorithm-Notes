// RRT*
// 学习重点：新点出现后，在附近可连接的节点中选总成本最低的父节点。
// 看看旧邻居能否经新点缩短路线，能就重连。
// 把重连造成的成本变化继续传给其后代。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <cmath>  // 距离、幂、平方根或数值判断
#include <random>  // 可复现实验的随机采样
#include <iomanip>  // 控制输出精度与格式
#include <stdexcept>  // 明确报告非法输入
#include <array>  // 固定长度坐标或障碍边界
#include <cstddef>  // 标准无符号大小类型

using namespace std;

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
struct Point { double x, y; };
using Obstacle = array<double,4>;
// 计算两点的欧氏距离，与采样空间坐标使用相同长度单位。
double distance(Point a, Point b) { return hypot(a.x-b.x,a.y-b.y); }

// 用线段参数区间检测闭矩形碰撞；接触障碍边界也视为碰撞。
bool collisionFree(Point a, Point b, const vector<Obstacle>& obstacles) {
    for (auto box : obstacles) {
        double low = 0, high = 1;
        for (int axis = 0; axis < 2; ++axis) {
            double position = axis == 0 ? a.x : a.y;
            double delta = axis == 0 ? b.x-a.x : b.y-a.y;
            if (abs(delta) < 1e-12) {
                if (position < box[axis] || position > box[axis+2]) { low = 1; high = 0; break; }
            } else {
                double t1 = (box[axis]-position)/delta, t2 = (box[axis+2]-position)/delta;
                if (t1 > t2) swap(t1,t2);
                low = max(low,t1);
                high = min(high,t2);
            }
        }
        if (low <= high) return false;
    }
    return true;
}

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
struct Tree {
    vector<Point> points;
    vector<int> parent;
    vector<double> cost;
    vector<Point> route;
};

// 在连续空间采样、扩展与检测碰撞；启用star时增加邻域选父和重连。
Tree plan(Point start, Point goal, const vector<Obstacle>& obstacles, int iterations, unsigned seed, bool star) {
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    if (iterations < 0) throw invalid_argument("negative iteration budget");
    if (!collisionFree(start,start,obstacles) || !collisionFree(goal,goal,obstacles)) {
        throw invalid_argument("endpoint inside obstacle");
    }
    mt19937 rng(seed);
    uniform_real_distribution<double> uniform(0,1);
    Tree tree{{start},{-1},{0},{}};
    vector<int> candidates;
    const double step = 0.9;
    for (int iteration = 0; iteration < iterations; ++iteration) {
        Point sample = uniform(rng) < 0.12 ? goal : Point{10*uniform(rng),10*uniform(rng)};
        int near = 0;
        for (int j = 1; j < static_cast<int>(tree.points.size()); ++j) {
            if (distance(tree.points[j],sample) < distance(tree.points[near],sample)) near = j;
        }
        Point base = tree.points[near];
        double length = distance(base,sample);
        if (length < 1e-10) continue;
        double ratio = min(1.0,step/length);
        Point point{base.x+ratio*(sample.x-base.x),base.y+ratio*(sample.y-base.y)};
        if (!collisionFree(base,point,obstacles)) continue;
        int n = static_cast<int>(tree.points.size());
        // 二维邻域半径随有效样本数收缩，演示常数不直接等于理论保证。
        double radius = min(2.5,9*sqrt(log(n+1.0)/(n+1.0)));
        vector<int> neighbors;
        if (star) for (int j = 0; j < n; ++j) if (distance(tree.points[j],point) <= radius) neighbors.push_back(j);
        int parent = near;
        for (int j : neighbors) {
            if (tree.cost[j]+distance(tree.points[j],point) < tree.cost[parent]+distance(tree.points[parent],point)
                && collisionFree(tree.points[j],point,obstacles)) parent = j;
        }
        tree.points.push_back(point);
        tree.parent.push_back(parent);
        tree.cost.push_back(tree.cost[parent]+distance(tree.points[parent],point));
        for (int j : neighbors) {
            double candidate = tree.cost[n]+distance(point,tree.points[j]);
            if (j == 0 || candidate+1e-9 >= tree.cost[j] || !collisionFree(point,tree.points[j],obstacles)) continue;
            // 只有经新节点严格更便宜且线段无碰撞，才重连旧节点。
            tree.parent[j] = n;
            tree.cost[j] = candidate;
            queue<int> changed;
            changed.push(j);
            // 把重连造成的成本变化传给全部后代，不能只改一个父指针。
            while (!changed.empty()) {
                // 读取先进先出的队首，保持发现的层次顺序。
                int p = changed.front();
                changed.pop();
                for (int child = 1; child <= n; ++child) if (tree.parent[child] == p) {
                    tree.cost[child] = tree.cost[p]+distance(tree.points[p],tree.points[child]);
                    changed.push(child);
                }
            }
        }
        if (distance(point,goal) <= step && collisionFree(point,goal,obstacles)) candidates.push_back(n);
    }
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (!candidates.empty()) {
        int best = *min_element(candidates.begin(),candidates.end(),[&](int a,int b) {
            return tree.cost[a]+distance(tree.points[a],goal) < tree.cost[b]+distance(tree.points[b],goal);
        });
        tree.route.push_back(goal);
        for (int u = best; u != -1; u = tree.parent[u]) tree.route.push_back(tree.points[u]);
        // 把反向收集的数据恢复为实际输出顺序。
        reverse(tree.route.begin(),tree.route.end());
    }
    return tree;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<Obstacle> obstacles{{3,2,6,7}};
    Tree tree = plan({1,1},{9,9},obstacles,250,7,true);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "nodes=" << tree.points.size() << '\n';
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (tree.route.empty()) { cout << "not found within budget\n"; return 0; }
    double total = 0;
    for (size_t i = 1; i < tree.route.size(); ++i) total += distance(tree.route[i-1],tree.route[i]);
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << fixed << setprecision(4) << "length=" << total << '\n';
    for (Point p : tree.route) cout << p.x << ',' << p.y << '\n';
}
