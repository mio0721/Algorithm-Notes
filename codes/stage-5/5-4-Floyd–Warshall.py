# Floyd–Warshall
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先填好直接边的距离表。

import math

# 逐轮开放中转点，计算全点对最短路，并检查是否存在负环。
def floyd_warshall(matrix):
    d = [row.copy() for row in matrix]
    # 中转点必须在最外层，表示本轮新允许使用哪个中转点。
    for k in range(len(d)):
        for i in range(len(d)):
            for j in range(len(d)):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    if any((d[i][i] < 0 for i in range(len(d)))):
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('检测到负环，不能直接把矩阵解释为有限最短距离')
    return d

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    inf = math.inf
    matrix = [[0, 3, 10, inf], [inf, 0, 4, 8], [inf, inf, 0, 2], [1, inf, inf, 0]]
    for row in floyd_warshall(matrix):
        # 输出计算结果，便于与课程例子或自行推演的答案核对。
        print(row)
if __name__ == '__main__':
    main()
