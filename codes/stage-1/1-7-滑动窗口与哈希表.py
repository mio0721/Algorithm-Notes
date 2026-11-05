s = "abcabcbbd"
last = {}
left = best = 0
for right, ch in enumerate(s):
    if ch in last:
        left = max(left, last[ch] + 1)
    last[ch] = right
    best = max(best, right - left + 1)
print(best)
