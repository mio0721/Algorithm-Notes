# DFS 与回溯
# Python 3；直接运行文件，修改示例数据可继续练习。
# 进入节点时把它加入当前路线。

g = [[1, 2], [3, 4], [5, 6], [7], [8, 5], [], [9], [], [9], []]
path, on_path = ([], set())

# 在当前分支中选择并递归探索，返回后恢复现场。
def dfs(u):
    # 把当前位置加入当前路线，不代表永久禁止其他路径使用它。
    path.append(u)
    on_path.add(u)
    if u == 9:
        # 输出计算结果，便于与课程例子或自行推演的答案核对。
        print([chr(65 + v) for v in path])
    else:
        for v in g[u]:
            if v not in on_path:
                dfs(v)
    # 返回上一层时恢复现场，让兄弟分支可以独立探索。
    path.pop()
    on_path.remove(u)
dfs(0)
