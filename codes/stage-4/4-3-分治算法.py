# 分治算法
# Python 3；直接运行文件，修改示例数据可继续练习。
# 把大数组拆成两小段。

# 用左右子问题分别排好序，再合并；返回新的有序列表。
def merge_sort(nums):
    a = list(nums)

    def sort(left, right):
        if right - left <= 1:
            return
        middle = (left + right) // 2
        sort(left, middle)
        sort(middle, right)
        merged, i, j = ([], left, middle)
        while i < middle and j < right:
            # 相等时优先取左边，保持相等元素的相对顺序。
            if a[i] <= a[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(a[j])
                j += 1
        # 合并完成后写回对应区间，左右子问题的有序结果才能变成整段有序。
        a[left:right] = merged + a[i:middle] + a[j:right]
    sort(0, len(a))
    return a

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print(merge_sort([8, 3, 7, 1, 9, 2, 6, 4, 5]))
if __name__ == '__main__':
    main()
