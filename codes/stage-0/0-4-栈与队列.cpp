// 栈与队列
// 学习重点：先根据任务选择“后来先出”或“先来先出”。
// 加入新数据。
// 确认容器非空，再查看并取出下一个数据。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <queue>  // 先进先出队列或优先队列
#include <stack>  // 后进先出的显式栈

using namespace std;

int queueFirst() {
    queue<int> q;
    q.push(4);
    q.push(7);
    // 先处理空容器或无结果情况，避免访问不存在的元素。
    if (q.empty()) return -1;
    // 队列的最早加入项先离开。
    int value = q.front();
    // 栈的最近加入项先离开；取出前必须确认非空。
    q.pop();
    return value;
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << "队首: " << queueFirst() << "\n";
    // 栈的最近加入项先离开；取出前必须确认非空。
    stack<int> s; s.push(4); s.push(7); cout << "栈顶: " << s.top() << "\n";
    return 0;
}
