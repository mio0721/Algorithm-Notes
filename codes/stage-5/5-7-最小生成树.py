# 最小生成树
# Python 3；直接运行文件，修改示例数据可继续练习。
# 把候选道路按价格从低到高排。

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
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = (b, a)
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.count -= 1
        return True

# 按权重考虑边，利用并查集只连接不同分量，返回树或森林及总成本。
def kruskal(n, edges):
    dsu, chosen, total = (DSU(n), [], 0)
    # 边按权重从小到大考虑；这里元组第一个字段就是权重。
    for weight, a, b in sorted(edges):
        take = dsu.union(a, b)
        # 只连接原本不同的集合，保证选择过程不成环。
        if take:
            chosen.append((a, b))
            total += weight
    return (total, chosen, dsu.count)

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    total, edges, count = kruskal(5, [(1, 0, 1), (4, 0, 2), (2, 1, 2), (3, 1, 3), (5, 2, 4), (1, 3, 4)])
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('MST' if count == 1 else 'minimum spanning forest', total, edges)
if __name__ == '__main__':
    main()
