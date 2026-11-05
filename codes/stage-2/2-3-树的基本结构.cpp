#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <functional>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int main() {
    TreeNode a(1), b(2), c(3), d(4);
    a.left=&b; a.right=&c; b.left=&d;
    cout << "根: " << a.val << "，左子节点: " << a.left->val << "，左孙节点: " << a.left->left->val << "\n";
    return 0;
}
