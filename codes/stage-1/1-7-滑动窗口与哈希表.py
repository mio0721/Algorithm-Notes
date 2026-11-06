# 滑动窗口与哈希表
# Python 3；直接运行文件，修改示例数据可继续练习。
# 右边每读到一个字符，检查它上次出现在哪里。

s = 'abcabcbbd'
last = {}
left = best = 0
for right, ch in enumerate(s):
    if ch in last:
        # 左边界只能前进，不能被窗口外的旧出现位置拉回。
        left = max(left, last[ch] + 1)
    # 每轮更新字符最后一次出现的位置，供下一次重复判断。
    last[ch] = right
    best = max(best, right - left + 1)
# 输出计算结果，便于与课程例子或自行推演的答案核对。
print(best)
