def sum_to(n):
    print("进入", n)
    if n == 0:
        return 0
    smaller = sum_to(n - 1)
    print("返回", n)
    return n + smaller

result = sum_to(2)
print("结果:", result)
