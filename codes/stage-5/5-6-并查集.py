# 并查集
# Python 3；直接运行文件，修改示例数据可继续练习。
# 每个点开始各自代表一个集合。

# 把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。
class DSU:

    # 初始化本对象保存的状态，后续方法将共同使用这些成员。
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    # 沿父指针找到集合代表，并压缩走过的路径以加速以后查询。
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    # 只合并不同根代表的集合，并维护根的大小与当前分量数量。
    def union(self, a, b):
        a, b = (self.find(a), self.find(b))
        # 两点已经同组，不再减少集合数量。
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = (b, a)
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.count -= 1
        return True

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    dsu = DSU(10)
    for a, b in [(0, 1), (2, 3), (1, 2), (4, 5), (6, 7), (5, 6), (8, 9), (3, 7), (0, 9), (1, 9)]:
        # 输出计算结果，便于与课程例子或自行推演的答案核对。
        print(a, b, 'merged:', dsu.union(a, b), 'components:', dsu.count)
    print('representatives:', [dsu.find(i) for i in range(10)])
if __name__ == '__main__':
    main()
