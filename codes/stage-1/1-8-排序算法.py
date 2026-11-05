a = [9, 3, 7, 1, 8, 2, 6, 4, 5]
for i in range(1, len(a)):
    value, j = a[i], i - 1
    while j >= 0 and a[j] > value:
        a[j + 1] = a[j]
        j -= 1
    a[j + 1] = value
print(a)
