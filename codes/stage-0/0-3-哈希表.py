# 哈希表 unordered_map 与 unordered_set
# Python 3；直接运行文件，修改示例数据可继续练习。
# 明确只需要判断存在，还是需要保存编号对应的值。

positions = {4: 0, 7: 1}
# 只查询已有键，不为了检查存在而插入默认记录。
print(positions.get(4, -1), positions.get(9, -1))
