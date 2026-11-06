// 最小生成树
// 学习重点：把候选道路按价格从低到高排。
// 两端还不连通就修这条路。
// 已经连通的两端再修会成环，跳过。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <utility>  // 二元组、交换或移动对象
#include <tuple>  // 多字段状态与字典序比较
#include <numeric>  // 连续编号初始化或累加

using namespace std;

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
class DSU {
    vector<int> parent, size;
public:
    int count;
    explicit DSU(int n) : parent(n), size(n,1), count(n) {
        iota(parent.begin(),parent.end(),0);
    }
    // 沿父指针找到集合代表，并压缩走过的路径以加速以后查询。
    int find(int u) {
        while (u != parent[u]) {
            parent[u] = parent[parent[u]];
            u = parent[u];
        }
        return u;
    }
    // 只合并不同根代表的集合，并维护根的大小与当前分量数量。
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

// 按权重考虑边，利用并查集只连接不同分量，返回树或森林及总成本。
tuple<long long, vector<pair<int,int>>, int> kruskal(int n, vector<tuple<int,int,int>> edges) {

    // 边按权重从小到大考虑；这里元组第一个字段就是权重。
    sort(edges.begin(),edges.end());
    DSU dsu(n);
    long long total = 0;
    vector<pair<int,int>> chosen;
    for (auto [weight,a,b] : edges) {
        // 只连接原本不同的集合，保证选择过程不成环。
        if (dsu.unite(a,b)) {
            total += weight;
            chosen.push_back({a,b});
        }
    }
    return {total,chosen,dsu.count};
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    auto [total,edges,count] = kruskal(5,{{1,0,1},{4,0,2},{2,1,2},{3,1,3},{5,2,4},{1,3,4}});
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << (count == 1 ? "MST" : "minimum spanning forest") << ", total=" << total << '\n';
    for (auto [a,b] : edges) cout << a << '-' << b << '\n';
}
