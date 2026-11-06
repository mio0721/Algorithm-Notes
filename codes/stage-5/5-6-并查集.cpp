// 并查集
// 学习重点：每个点开始各自代表一个集合。
// 沿父指针找到根，根就是代表。
// 需要连接两组时，把两个根合并，并让以后找根更短。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <utility>  // 二元组、交换或移动对象
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
            // 路径减半只让节点更接近同一个根，不改变它所属集合。
            parent[u] = parent[parent[u]];
            u = parent[u];
        }
        return u;
    }
    // 只合并不同根代表的集合，并维护根的大小与当前分量数量。
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        // 两点已经同组，不再减少集合数量。
        if (a == b) return false;
        if (size[a] < size[b]) swap(a,b);
        parent[b] = a;
        size[a] += size[b];
        --count;
        return true;
    }
};

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    DSU dsu(10);
    for (auto [a,b] : vector<pair<int,int>>{{0,1},{2,3},{1,2},{4,5},{6,7},{5,6},{8,9},{3,7},{0,9},{1,9}}) {
        bool merged = dsu.unite(a,b);
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << a << '-' << b << ": " << (merged ? "merged" : "already connected")
             << ", components=" << dsu.count << '\n';
    }
    for (int u = 0; u < 10; ++u) cout << u << "->" << dsu.find(u) << ' ';
    cout << '\n';
}
