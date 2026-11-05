class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
print("根:", root.val, "左子节点:", root.left.val, "左孙节点:", root.left.left.val)
