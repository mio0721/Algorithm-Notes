// 堆与优先队列
// 学习重点：把任务和优先级一起加入堆。
// 每次读取堆顶。
// 移除已处理任务，堆会重新保证顶端最优。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <vector>  // 动态数组、邻接表或状态表
#include <queue>  // 先进先出队列或优先队列
#include <functional>  // 递归函数包装或堆比较器

using namespace std;

int smallest() {
    // 最小堆先处理较小代价；C++的比较器方向与默认大根堆不同。
    priority_queue<int, vector<int>, greater<int>> pq;
    pq.push(5);
    pq.push(2);
    int x = pq.top();
    pq.pop();
    return x;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "最小值: " << smallest() << "\n";
    return 0;
}
