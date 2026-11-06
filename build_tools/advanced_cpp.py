"""Readable, standalone C++17 teaching programs for stages 4–6."""
HEADER = '''#include <algorithm>
#include <array>
#include <cmath>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
using namespace std;

'''
SOURCES = {}
SOURCES['4.1'] = r'''
vector<vector<int>> subsets(const vector<int>& nums) {
    vector<vector<int>> answer;
    vector<int> path;
    function<void(int)> visit = [&](int start) {
        answer.push_back(path);  // Copy: later undo must not change saved answers.
        for (int i = start; i < static_cast<int>(nums.size()); ++i) {
            path.push_back(nums[i]);
            visit(i + 1);
            path.pop_back();
        }
    };
    visit(0);
    return answer;
}

int main() {
    for (const auto& subset : subsets({1, 2, 3, 4})) {
        cout << "[ ";
        for (int value : subset) cout << value << ' ';
        cout << "]\n";
    }
}
'''
SOURCES['4.2'] = r'''
vector<pair<int, int>> selectIntervals(vector<pair<int, int>> intervals) {
    for (auto [start, end] : intervals) {
        if (end < start) throw invalid_argument("end before start");
    }
    sort(intervals.begin(), intervals.end(), [](auto a, auto b) {
        return tie(a.second, a.first) < tie(b.second, b.first);
    });
    vector<pair<int, int>> chosen;
    long long lastEnd = numeric_limits<long long>::lowest();
    for (auto [start, end] : intervals) {
        if (start >= lastEnd) {
            chosen.push_back({start, end});
            lastEnd = end;
        }
    }
    return chosen;
}

int main() {
    auto result = selectIntervals({{1,4}, {3,5}, {0,6}, {5,7}, {3,9},
                                   {5,9}, {6,10}, {8,11}, {8,9}});
    for (auto [start, end] : result) cout << '[' << start << ',' << end << ")\n";
    cout << "count=" << result.size() << '\n';
}
'''
SOURCES['4.3'] = r'''
void mergeSort(vector<int>& nums) {
    vector<int> buffer(nums.size());
    function<void(int, int)> sortRange = [&](int left, int right) {
        if (right - left <= 1) return;
        int middle = left + (right - left) / 2;
        sortRange(left, middle);
        sortRange(middle, right);
        int a = left, b = middle, output = left;
        while (a < middle && b < right) {
            buffer[output++] = nums[a] <= nums[b] ? nums[a++] : nums[b++];
        }
        while (a < middle) buffer[output++] = nums[a++];
        while (b < right) buffer[output++] = nums[b++];
        copy(buffer.begin() + left, buffer.begin() + right, nums.begin() + left);
    };
    sortRange(0, static_cast<int>(nums.size()));
}

int main() {
    vector<int> nums{8, 3, 7, 1, 9, 2, 6, 4, 5};
    mergeSort(nums);
    for (int value : nums) cout << value << ' ';
    cout << '\n';
}
'''
SOURCES['4.4'] = r'''
long long climbStairs(int n) {
    if (n < 0 || n > 90) throw invalid_argument("n must be in [0,90]");
    vector<long long> dp(n + 1);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i - 1];
        if (i >= 2) dp[i] += dp[i - 2];
    }
    return dp[n];
}

int main() {
    for (int n : {0, 1, 5, 9}) cout << n << ": " << climbStairs(n) << '\n';
}
'''
SOURCES['4.5'] = r'''
long long knapsack(const vector<int>& weights, const vector<int>& values, int capacity) {
    if (weights.size() != values.size() || capacity < 0) {
        throw invalid_argument("invalid dimensions");
    }
    vector<long long> dp(capacity + 1, 0);
    for (size_t i = 0; i < weights.size(); ++i) {
        if (weights[i] <= 0) throw invalid_argument("weights must be positive");
        // Descending capacities read the previous item's row.
        for (int c = capacity; c >= weights[i]; --c) {
            dp[c] = max(dp[c], dp[c - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}

int main() {
    cout << knapsack({2, 3, 4, 5}, {3, 4, 5, 8}, 9) << '\n';
    cout << knapsack({2}, {3}, 4) << '\n'; // 3, not 6: each item at most once.
}
'''
SOURCES['4.6'] = r'''
string lcs(const string& a, const string& b) {
    int m = static_cast<int>(a.size()), n = static_cast<int>(b.size());
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            dp[i][j] = a[i - 1] == b[j - 1]
                ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    string result;
    while (m > 0 && n > 0) {
        if (a[m - 1] == b[n - 1]) {
            result.push_back(a[--m]);
            --n;
        } else if (dp[m - 1][n] >= dp[m][n - 1]) {
            --m;
        } else {
            --n;
        }
    }
    reverse(result.begin(), result.end());
    return result;
}

int main() {
    string result = lcs("ABCBDAB", "BDCABA");
    cout << result.size() << ' ' << result << '\n';
}
'''
SOURCES['5.1'] = r'''
vector<vector<int>> components(const vector<vector<int>>& graph) {
    vector<bool> visited(graph.size(), false);
    vector<vector<int>> groups;
    for (int start = 0; start < static_cast<int>(graph.size()); ++start) {
        if (visited[start]) continue;
        groups.push_back({});
        vector<int> stack{start};
        visited[start] = true;
        while (!stack.empty()) {
            int u = stack.back();
            stack.pop_back();
            groups.back().push_back(u);
            for (int v : graph[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    stack.push_back(v);
                }
            }
        }
    }
    return groups;
}

int main() {
    vector<vector<int>> graph(10);
    for (auto [u, v] : vector<pair<int,int>>{{0,1},{1,2},{2,3},{4,5},{5,6},{7,8}}) {
        graph[u].push_back(v);
        graph[v].push_back(u);
    }
    auto result = components(graph);
    cout << "components=" << result.size() << '\n';
    for (const auto& group : result) {
        for (int u : group) cout << char('A' + u) << ' ';
        cout << '\n';
    }
}
'''
SOURCES['5.2'] = r'''
using WeightedGraph = vector<vector<pair<int, int>>>;
const long long INF = numeric_limits<long long>::max() / 4;

pair<vector<long long>, vector<int>> dijkstra(const WeightedGraph& graph, int start) {
    for (const auto& edges : graph) {
        for (auto [v, weight] : edges) {
            if (weight < 0) throw invalid_argument("negative edge");
        }
    }
    vector<long long> distance(graph.size(), INF);
    vector<int> parent(graph.size(), -1);
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> heap;
    distance.at(start) = 0;
    heap.push({0, start});
    while (!heap.empty()) {
        auto [cost, u] = heap.top();
        heap.pop();
        if (cost != distance[u]) continue;
        for (auto [v, weight] : graph[u]) {
            if (cost + weight < distance[v]) {
                distance[v] = cost + weight;
                parent[v] = u;
                heap.push({distance[v], v});
            }
        }
    }
    return {distance, parent};
}

int main() {
    WeightedGraph graph(10);
    for (auto [u,v,w] : vector<tuple<int,int,int>>{
            {0,1,4},{0,2,1},{2,1,2},{1,3,1},{2,4,5},{3,5,3},
            {4,5,1},{5,6,2},{6,7,1},{7,8,2},{8,9,1}}) graph[u].push_back({v,w});
    auto [distance, parent] = dijkstra(graph, 0);
    for (int u = 0; u < 10; ++u) cout << char('A'+u) << ": " << distance[u] << '\n';
    vector<int> route;
    if (distance[9] != INF) {
        for (int u = 9; u != -1; u = parent[u]) route.push_back(u);
        reverse(route.begin(), route.end());
    }
    for (int u : route) cout << char('A'+u) << ' ';
    cout << '\n';
}
'''
GRID = r'''
using Cell = pair<int, int>;
vector<Cell> astar(const vector<string>& grid, Cell start, Cell goal, bool useHeuristic = true) {
    if (grid.empty() || grid[0].empty()) throw invalid_argument("empty map");
    int rows = static_cast<int>(grid.size()), cols = static_cast<int>(grid[0].size());
    for (const auto& row : grid) if (static_cast<int>(row.size()) != cols) throw invalid_argument("ragged map");
    auto valid = [&](Cell p) {
        return p.first >= 0 && p.first < rows && p.second >= 0 && p.second < cols;
    };
    if (!valid(start) || !valid(goal)) throw invalid_argument("endpoint outside map");
    if (grid[start.first][start.second] == '#' || grid[goal.first][goal.second] == '#') return {};
    auto heuristic = [&](Cell p) {
        return useHeuristic ? abs(p.first-goal.first)+abs(p.second-goal.second) : 0;
    };
    map<Cell,int> distance;
    map<Cell,Cell> parent;
    using Entry = tuple<int,int,Cell>;
    priority_queue<Entry,vector<Entry>,greater<Entry>> heap;
    distance[start] = 0;
    heap.push({heuristic(start),0,start});
    while (!heap.empty()) {
        auto [estimate,cost,u] = heap.top();
        heap.pop();
        if (distance[u] != cost) continue;
        if (u == goal) {
            vector<Cell> route{u};
            while (u != start) {
                u = parent.at(u);
                route.push_back(u);
            }
            reverse(route.begin(),route.end());
            return route;
        }
        for (Cell delta : vector<Cell>{{-1,0},{1,0},{0,-1},{0,1}}) {
            Cell v{u.first+delta.first,u.second+delta.second};
            if (!valid(v) || grid[v.first][v.second] == '#') continue;
            if (!distance.count(v) || cost+1 < distance[v]) {
                distance[v] = cost+1;
                parent[v] = u;
                heap.push({cost+1+heuristic(v),cost+1,v});
            }
        }
    }
    return {};
}
'''
GRID_MAIN = r'''
int main() {
    vector<string> grid{".........", ".###.###.", "...#.....", "...#.###.", ".........", "..###...."};
    auto route = astar(grid,{0,0},{5,8});
    if (route.empty()) { cout << "unreachable\n"; return 0; }
    cout << "steps=" << route.size()-1 << '\n';
    for (auto [r,c] : route) if (grid[r][c] != '#') grid[r][c] = '*';
    for (const auto& row : grid) cout << row << '\n';
}
'''
SOURCES['5.3'] = GRID + GRID_MAIN
SOURCES['6.1'] = GRID + GRID_MAIN.replace('auto route = astar(grid,{0,0},{5,8});', '''auto uniform = astar(grid,{0,0},{5,8},false);
    auto route = astar(grid,{0,0},{5,8},true);
    cout << "same optimal length=" << (uniform.size() == route.size()) << '\\n';''')
SOURCES['5.4'] = r'''
const long long INF = numeric_limits<long long>::max()/4;
vector<vector<long long>> floyd(vector<vector<long long>> distance) {
    int n = static_cast<int>(distance.size());
    for (const auto& row : distance) if (static_cast<int>(row.size()) != n) throw invalid_argument("not square");
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (distance[i][k] != INF && distance[k][j] != INF) {
                    distance[i][j] = min(distance[i][j], distance[i][k]+distance[k][j]);
                }
            }
        }
    }
    for (int i = 0; i < n; ++i) if (distance[i][i] < 0) throw invalid_argument("negative cycle");
    return distance;
}

int main() {
    vector<vector<long long>> distance{{0,3,10,INF},{INF,0,4,8},{INF,INF,0,2},{1,INF,INF,0}};
    for (const auto& row : floyd(distance)) {
        for (long long cost : row) {
            if (cost == INF) cout << "INF "; else cout << cost << ' ';
        }
        cout << '\n';
    }
}
'''
SOURCES['5.5'] = r'''
vector<int> topologicalSort(const vector<vector<int>>& graph) {
    vector<int> indegree(graph.size());
    for (const auto& edges : graph) for (int v : edges) ++indegree[v];
    queue<int> ready;
    for (int u = 0; u < static_cast<int>(graph.size()); ++u) if (!indegree[u]) ready.push(u);
    vector<int> order;
    while (!ready.empty()) {
        int u = ready.front();
        ready.pop();
        order.push_back(u);
        for (int v : graph[u]) if (--indegree[v] == 0) ready.push(v);
    }
    if (order.size() != graph.size()) throw invalid_argument("dependency cycle");
    return order;
}

int main() {
    vector<vector<int>> graph{{2,3},{3},{4},{4,5},{6},{7},{8},{8},{9},{}};
    for (int u : topologicalSort(graph)) cout << char('A'+u) << ' ';
    cout << '\n';
    try {
        topologicalSort({{1},{0}});
    } catch (const invalid_argument& error) {
        cout << error.what() << '\n';
    }
}
'''
DSU = r'''
class DSU {
    vector<int> parent, size;
public:
    int count;
    explicit DSU(int n) : parent(n), size(n,1), count(n) {
        iota(parent.begin(),parent.end(),0);
    }
    int find(int u) {
        while (u != parent[u]) {
            parent[u] = parent[parent[u]];
            u = parent[u];
        }
        return u;
    }
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a,b);
        parent[b] = a;
        size[a] += size[b];
        --count;
        return true;
    }
};
'''
SOURCES['5.6'] = DSU + r'''
int main() {
    DSU dsu(10);
    for (auto [a,b] : vector<pair<int,int>>{{0,1},{2,3},{1,2},{4,5},{6,7},{5,6},{8,9},{3,7},{0,9},{1,9}}) {
        bool merged = dsu.unite(a,b);
        cout << a << '-' << b << ": " << (merged ? "merged" : "already connected")
             << ", components=" << dsu.count << '\n';
    }
    for (int u = 0; u < 10; ++u) cout << u << "->" << dsu.find(u) << ' ';
    cout << '\n';
}
'''
SOURCES['5.7'] = DSU + r'''
tuple<long long, vector<pair<int,int>>, int> kruskal(int n, vector<tuple<int,int,int>> edges) {
    // Each tuple is (weight, start, end), so natural sorting uses weight first.
    sort(edges.begin(),edges.end());
    DSU dsu(n);
    long long total = 0;
    vector<pair<int,int>> chosen;
    for (auto [weight,a,b] : edges) {
        if (dsu.unite(a,b)) {
            total += weight;
            chosen.push_back({a,b});
        }
    }
    return {total,chosen,dsu.count};
}

int main() {
    auto [total,edges,count] = kruskal(5,{{1,0,1},{4,0,2},{2,1,2},{3,1,3},{5,2,4},{1,3,4}});
    cout << (count == 1 ? "MST" : "minimum spanning forest") << ", total=" << total << '\n';
    for (auto [a,b] : edges) cout << a << '-' << b << '\n';
}
'''
SOURCES['6.2'] = r'''
using Cell = pair<int,int>;
using Key = pair<double,double>;
const double INF = numeric_limits<double>::infinity();

class DStarLite {
    vector<string> grid;
    Cell start, goal, last;
    double km = 0;
    map<Cell,double> g, rhs;
    map<Cell,Key> pending;
    using Entry = pair<Key,Cell>;
    priority_queue<Entry,vector<Entry>,greater<Entry>> heap;

    double value(const map<Cell,double>& table, Cell u) const {
        auto it = table.find(u);
        return it == table.end() ? INF : it->second;
    }
    double heuristic(Cell a, Cell b) const {
        return abs(a.first-b.first)+abs(a.second-b.second);
    }
    Key key(Cell u) const {
        double best = min(value(g,u),value(rhs,u));
        return {best+heuristic(start,u)+km,best};
    }
    vector<Cell> neighbors(Cell u) const {
        vector<Cell> result;
        for (auto [dr,dc] : vector<Cell>{{-1,0},{1,0},{0,-1},{0,1}}) {
            Cell v{u.first+dr,u.second+dc};
            if (v.first >= 0 && v.first < static_cast<int>(grid.size()) &&
                v.second >= 0 && v.second < static_cast<int>(grid[0].size())) result.push_back(v);
        }
        return result;
    }
    double cost(Cell a, Cell b) const {
        return grid[a.first][a.second] == '#' || grid[b.first][b.second] == '#' ? INF : 1;
    }
    void push(Cell u) {
        pending[u] = key(u);
        heap.push({pending[u],u});
    }
    Key top() {
        while (!heap.empty()) {
            auto [k,u] = heap.top();
            auto it = pending.find(u);
            if (it != pending.end() && it->second == k) return k;
            heap.pop();
        }
        return {INF,INF};
    }
    void update(Cell u) {
        if (u != goal) {
            rhs[u] = INF;
            for (Cell v : neighbors(u)) rhs[u] = min(rhs[u],cost(u,v)+value(g,v));
        }
        pending.erase(u);
        if (value(g,u) != value(rhs,u)) push(u);
    }
public:
    DStarLite(vector<string> map, Cell s, Cell t) : grid(move(map)),start(s),goal(t),last(s) {
        if (grid.empty() || grid[0].empty()) throw invalid_argument("empty map");
        for (const auto& row : grid) if (row.size() != grid[0].size()) throw invalid_argument("ragged map");
        for (Cell u : {start,goal}) {
            if (u.first < 0 || u.first >= static_cast<int>(grid.size()) ||
                u.second < 0 || u.second >= static_cast<int>(grid[0].size()) || grid[u.first][u.second] == '#') {
                throw invalid_argument("invalid endpoint");
            }
        }
        rhs[goal] = 0;
        push(goal);
    }
    void repair() {
        while (top() < key(start) || value(rhs,start) != value(g,start)) {
            auto [old,u] = heap.top();
            heap.pop();
            pending.erase(u);
            if (old < key(u)) {
                push(u);
            } else if (value(g,u) > value(rhs,u)) {
                g[u] = value(rhs,u);
                for (Cell p : neighbors(u)) update(p);
            } else {
                g[u] = INF;
                update(u);
                for (Cell p : neighbors(u)) update(p);
            }
        }
    }
    void change(Cell u, bool blocked) {
        if (u == start || u == goal) throw invalid_argument("cannot block endpoint");
        grid.at(u.first).at(u.second) = blocked ? '#' : '.';
        update(u);
        for (Cell p : neighbors(u)) update(p);
    }
    void moveStart(Cell s) {
        km += heuristic(last,s);
        start = last = s;
    }
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

int main() {
    DStarLite planner({".........",".###.###.","...#.....","...#.###.",".........","..###...."},{0,0},{5,8});
    planner.repair();
    auto before = planner.path();
    cout << "initial steps=" << before.size()-1 << '\n';
    Cell changed = before.at(before.size()/2);
    planner.change(changed,true);
    planner.repair();
    auto after = planner.path();
    if (after.empty()) cout << "unreachable\n";
    else cout << "repaired steps=" << after.size()-1 << '\n';
    planner.change(changed,false);
    planner.repair();
    cout << "restored steps=" << planner.path().size()-1 << '\n';
}
'''
RRT = r'''
struct Point { double x, y; };
using Obstacle = array<double,4>; // left, bottom, right, top
double distance(Point a, Point b) { return hypot(a.x-b.x,a.y-b.y); }

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
        if (low <= high) return false; // Contact counts as collision.
    }
    return true;
}

struct Tree {
    vector<Point> points;
    vector<int> parent;
    vector<double> cost;
    vector<Point> route;
};

Tree plan(Point start, Point goal, const vector<Obstacle>& obstacles, int iterations, unsigned seed, bool star) {
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
            tree.parent[j] = n;
            tree.cost[j] = candidate;
            queue<int> changed;
            changed.push(j);
            while (!changed.empty()) {
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
    if (!candidates.empty()) {
        int best = *min_element(candidates.begin(),candidates.end(),[&](int a,int b) {
            return tree.cost[a]+distance(tree.points[a],goal) < tree.cost[b]+distance(tree.points[b],goal);
        });
        tree.route.push_back(goal);
        for (int u = best; u != -1; u = tree.parent[u]) tree.route.push_back(tree.points[u]);
        reverse(tree.route.begin(),tree.route.end());
    }
    return tree;
}
'''
RRT_MAIN = r'''
int main() {
    vector<Obstacle> obstacles{{3,2,6,7}};
    Tree tree = plan({1,1},{9,9},obstacles,250,7,STAR);
    cout << "nodes=" << tree.points.size() << '\n';
    if (tree.route.empty()) { cout << "not found within budget\n"; return 0; }
    double total = 0;
    for (size_t i = 1; i < tree.route.size(); ++i) total += distance(tree.route[i-1],tree.route[i]);
    cout << fixed << setprecision(4) << "length=" << total << '\n';
    for (Point p : tree.route) cout << p.x << ',' << p.y << '\n';
}
'''
SOURCES['6.3'] = RRT + RRT_MAIN.replace('STAR','false')
SOURCES['6.4'] = RRT + RRT_MAIN.replace('STAR','true')
SOURCES['6.5'] = r'''
array<double,3> trajectory(double displacement, double duration, double time) {
    if (duration <= 0 || time < 0 || time > duration) throw invalid_argument("invalid time");
    double tau = time/duration;
    double s = displacement*(10*pow(tau,3)-15*pow(tau,4)+6*pow(tau,5));
    double v = displacement/duration*(30*pow(tau,2)-60*pow(tau,3)+30*pow(tau,4));
    double a = displacement/(duration*duration)*(60*tau-180*pow(tau,2)+120*pow(tau,3));
    return {s,v,a};
}

int main() {
    double displacement = 10, maxVelocity = 2, maxAcceleration = 1;
    double duration = max(15.0/8*abs(displacement)/maxVelocity,
                          sqrt(10*sqrt(3.0)/3*abs(displacement)/maxAcceleration));
    cout << fixed << setprecision(6) << "T=" << duration << '\n';
    cout << "t,s,v,a\n";
    for (int i = 0; i <= 40; ++i) {
        double time = duration*i/40;
        auto [s,v,a] = trajectory(displacement,duration,time);
        cout << time << ',' << s << ',' << v << ',' << a << '\n';
    }
}
'''

def code(id):
    return HEADER + SOURCES[id].strip() + '\n'
