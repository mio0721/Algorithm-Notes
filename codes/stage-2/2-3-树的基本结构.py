# 树的基本结构
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先找到整个层级的起点，也就是根。

# 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
class TreeNode:

    # 初始化本对象保存的状态，后续方法将共同使用这些成员。
    def __init__(self, value):
        self.val = value
        # 这里只记录父子关系；空孩子表示对应方向没有节点。
        self.left = None
        self.right = None
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
print('根:', root.val, '左子节点:', root.left.val, '左孙节点:', root.left.left.val)
