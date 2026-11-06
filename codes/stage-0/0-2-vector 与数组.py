# vector 与数组
# Python 3；直接运行文件，修改示例数据可继续练习。
# 把数据按顺序放进容器。

# 保存一串按位置编号的数据，编号从0开始。
nums = []
# 把新读数追加到末尾；容量不足时可能搬迁底层存储。
nums.append(4)
nums.append(7)
for index, value in enumerate(nums):
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(f'{index}: {value}')
