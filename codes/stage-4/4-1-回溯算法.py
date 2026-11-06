# 回溯算法
# Python 3；直接运行文件，修改示例数据可继续练习。
# 保存当前已经选出的装备。

# 枚举当前路径和所有后续扩展，返回每个合法子集的一份独立副本。
def subsets(nums):
    answer, path = ([], [])

    # 在当前分支中选择并递归探索，返回后恢复现场。
    def visit(index):
        # 立即保存当前选择的副本，包含什么也不选的空集。
        answer.append(path.copy())
        for i in range(index, len(nums)):
            path.append(nums[i])
            # 只从后续下标选择，避免同一个组合换顺序后重复输出。
            visit(i + 1)
            # 撤销本轮选择，恢复进入分支前的状态。
            path.pop()
    visit(0)
    return answer

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    for row in subsets([1, 2, 3, 4]):
        # 输出计算结果，便于与课程例子或自行推演的答案核对。
        print(row)
if __name__ == '__main__':
    main()
