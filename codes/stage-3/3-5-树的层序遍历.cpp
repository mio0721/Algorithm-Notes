// 树的层序遍历
// 学习重点：当前队列里保存本层节点。
// 先记住队列长度，恰好取出这么多个节点。
// 把孩子加入队尾，留给下一轮。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列

using namespace std;

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    vector<vector<int>> children = {
        {1, 2},
        {3, 4},
        {5, 6},
        {7},
        {8},
        {},
        {9},
        {},
        {},
        {}
    };
    queue<int> pending;
    pending.push(0);

    // 反复取出一个待处理状态；集合耗尽时，本轮搜索结束。
    while (!pending.empty()) {

        int count = static_cast<int>(pending.size());
        for (int i = 0; i < count; ++i) {
            // 读取先进先出的队首，保持发现的层次顺序。
            int u = pending.front();
            pending.pop();
            // 输出计算结果，便于与课程例子或自行推演的答案核对。
            cout << u + 1 << " ";

            for (int v : children[u]) {
                pending.push(v);
            }
        }
        // 输出计算结果，便于与课程例子或自行推演的答案核对。
        cout << endl;
    }
    return 0;
}
