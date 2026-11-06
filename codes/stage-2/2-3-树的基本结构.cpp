// 树的基本结构
// 学习重点：先找到整个层级的起点，也就是根。
// 从每个节点连接到它的孩子。
// 沿父子关系逐层或逐条分支访问。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出

using namespace std;

// 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
struct TreeNode {
    int val;
    // 这里只记录父子关系；空孩子表示对应方向没有节点。
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    TreeNode a(1), b(2), c(3), d(4);
    // 这里只记录父子关系；空孩子表示对应方向没有节点。
    a.left=&b; a.right=&c; b.left=&d;
    cout << "根: " << a.val << "，左子节点: " << a.left->val << "，左孙节点: " << a.left->left->val << "\n";
    return 0;
}
