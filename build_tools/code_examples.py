"""Standalone teaching examples; each program runs without input."""
CPP_MAIN={
'0.1':'cout << linearSearch(vector<int>{2, 4, 6, 8}, 6) << "\\n";',
'0.2':'auto nums = makeValues();\n    for (size_t i = 0; i < nums.size(); ++i) cout << i << ": " << nums[i] << "\\n";',
'0.3':'unordered_map<int,int> mp{{4,0},{7,1}};\n    cout << findIndex(mp,4) << " " << findIndex(mp,9) << "\\n";',
'0.4':'cout << "队首: " << queueFirst() << "\\n";\n    stack<int> s; s.push(4); s.push(7); cout << "栈顶: " << s.top() << "\\n";',
'0.5':'cout << "最小值: " << smallest() << "\\n";',
'1.1':'vector<int> a{-5,-1,0,3,5,9,12,16,20};\n    cout << search(a,9) << "\\n";',
'1.2':'vector<int> a{1,3,5,6,8,10,12,15,18};\n    cout << searchInsert(a,7) << "\\n";',
'1.3':'vector<int> a{1,2,4,6,9,12,15,19,23};\n    for (int i : twoSum(a,17)) cout << i << " ";\n    cout << "\\n";',
'1.4':'vector<int> a{0,0,1,1,2,2,3,3,4};\n    int k=removeDuplicates(a);\n    cout << "长度: " << k << "，有效元素: ";\n    for(int i=0;i<k;++i) cout << a[i] << " ";\n    cout << "\\n";',
'1.5':'vector<int> a{3,2,2,3,4,3,5,2,3};\n    int k=removeElement(a,3);\n    cout << "长度: " << k << "，有效元素: ";\n    for(int i=0;i<k;++i) cout << a[i] << " ";\n    cout << "\\n";',
'1.6':'vector<int> a{2,3,1,2,4,3,1,2,5};\n    cout << minSubArrayLen(7,a) << "\\n";',
'2.1':'cout << "sum(3) = " << sum(3) << "\\n";',
'2.2':'int result=sum(2);\n    cout << "结果: " << result << "\\n";',
'2.3':'TreeNode a(1), b(2), c(3), d(4);\n    a.left=&b; a.right=&c; b.left=&d;\n    cout << "根: " << a.val << "，左子节点: " << a.left->val << "，左孙节点: " << a.left->left->val << "\\n";',
}
CPP_OVERRIDE={
'2.4':'''struct Edge { int to; int weight; };
int main() {
    vector<vector<Edge>> graph(3);
    graph[0].push_back({1,4});
    graph[1].push_back({2,3});
    for (int u=0; u<3; ++u)
        for (const auto& edge : graph[u])
            cout << u << " -> " << edge.to << "，权重 " << edge.weight << "\\n";
}''',
'2.5':'''int main() {
    vector<vector<int>> graph(8);
    auto addEdge = [&](int a, int b) { graph[a].push_back(b); graph[b].push_back(a); };
    for (auto edge : vector<pair<int,int>>{{0,1},{0,2},{1,3},{1,4},{2,5},{2,6},{6,7},{4,7}})
        addEdge(edge.first, edge.second);
    for (int i=0; i<8; ++i) {
        cout << i << ": ";
        for (int neighbor : graph[i]) cout << neighbor << " ";
        cout << "\\n";
    }
}''',
'2.6':'''int main() {
    vector<vector<int>> graph{{1,2},{0,2},{0,1}};
    vector<bool> visited(graph.size(), false);
    queue<int> pending;
    int start=0; visited[start]=true; pending.push(start);
    while (!pending.empty()) {
        int u=pending.front(); pending.pop();
        cout << "访问 " << char('A'+u) << "\\n";
        for (int v : graph[u]) if (!visited[v]) {
            visited[v]=true; pending.push(v);
        }
    }
}'''
}
PYTHON={
'0.1':'''def linear_search(nums, target):
    for index, value in enumerate(nums):
        if value == target:
            return index
    return -1

print(linear_search([2, 4, 6, 8], 6))''',
'0.2':'''nums = []
nums.append(4)
nums.append(7)
for index, value in enumerate(nums):
    print(f"{index}: {value}")''',
'0.3':'''positions = {4: 0, 7: 1}
print(positions.get(4, -1), positions.get(9, -1))''',
'0.4':'''from collections import deque
stack = [4, 7]
queue = deque([4, 7])
print("栈顶:", stack.pop())
print("队首:", queue.popleft())''',
'0.5':'''import heapq
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
print("最小值:", heapq.heappop(heap))''',
'1.1':'''def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

print(search([-5, -1, 0, 3, 5, 9, 12, 16, 20], 9))''',
'1.2':'''def search_insert(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

print(search_insert([1, 3, 5, 6, 8, 10, 12, 15, 18], 7))''',
'1.3':'''def two_sum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []

print(two_sum([1, 2, 4, 6, 9, 12, 15, 19, 23], 17))''',
'1.4':'''def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

nums = [0, 0, 1, 1, 2, 2, 3, 3, 4]
k = remove_duplicates(nums)
print("长度:", k, "有效元素:", nums[:k])''',
'1.5':'''def remove_element(nums, value):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != value:
            nums[slow] = nums[fast]
            slow += 1
    return slow

nums = [3, 2, 2, 3, 4, 3, 5, 2, 3]
k = remove_element(nums, 3)
print("长度:", k, "有效元素:", nums[:k])''',
'1.6':'''def min_subarray_len(target, nums):
    left = total = 0
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == len(nums) + 1 else best

print(min_subarray_len(7, [2, 3, 1, 2, 4, 3, 1, 2, 5]))''',
'2.1':'''def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)

print("sum(3) =", sum_to(3))''',
'2.2':'''def sum_to(n):
    print("进入", n)
    if n == 0:
        return 0
    smaller = sum_to(n - 1)
    print("返回", n)
    return n + smaller

result = sum_to(2)
print("结果:", result)''',
'2.3':'''class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
print("根:", root.val, "左子节点:", root.left.val, "左孙节点:", root.left.left.val)''',
'2.4':'''graph = [[], [], []]
graph[0].append((1, 4))  # 终点、权重
graph[1].append((2, 3))
for start, edges in enumerate(graph):
    for end, weight in edges:
        print(f"{start} -> {end}，权重 {weight}")''',
'2.5':'''graph = [[] for _ in range(8)]
for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7), (4, 7)]:
    graph[a].append(b)
    graph[b].append(a)
for node, neighbors in enumerate(graph):
    print(f"{node}: {neighbors}")''',
'2.6':'''from collections import deque
graph = [[1, 2], [0, 2], [0, 1]]
visited = [False] * len(graph)
pending = deque([0])
visited[0] = True
while pending:
    node = pending.popleft()
    print("访问", chr(ord("A") + node))
    for neighbor in graph[node]:
        if not visited[neighbor]:
            visited[neighbor] = True
            pending.append(neighbor)'''
}

def code_for(item):
    id=item[0]
    head='#include <iostream>\n#include <vector>\n#include <queue>\n#include <stack>\n#include <unordered_map>\n#include <functional>\n#include <algorithm>\nusing namespace std;\n\n'
    body=CPP_OVERRIDE.get(id)
    if body is None:
        body=item[7]+'\n\nint main() {\n    '+CPP_MAIN[id]+'\n    return 0;\n}'
    return head+body+'\n', PYTHON[id]+'\n'
