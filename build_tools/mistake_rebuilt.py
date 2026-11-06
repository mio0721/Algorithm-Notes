"""逐个编写的错误片段与对应状态；帧只描述该片段确实会发生的行为。"""

def f(values, text, active=(), pointers=None, warning=False):
    return {'cells': list(map(str, values)), 'indexed': True, 'active': list(active),
            'pointers': pointers or {}, 'text': text, 'warning': warning}

CASES = {
 '0.2': [
  ('把长度当作最后下标', '数组 [10,20,30] 长度为 3。', 'int x = nums[nums.size()];', 'int x = nums.back(); // 已确认数组非空', '长度为 3 时合法下标是 0、1、2；访问 3 越界。', [
   f([10,20,30], '长度为 3，先检查有效下标。'),
   f([10,20,30], '最后一个元素位于下标 2。', [2]),
   f([10,20,30], '出错：nums[3] 越过末尾，属于未定义行为，不能假设会返回某个值。', warning=True)]),
  ('扩容后继续使用旧引用', '当容量已满时，push_back 可能重新分配存储。', 'int& first = nums[0];\nnums.push_back(40);\ncout << first; // 旧引用可能失效', 'nums.push_back(40);\nint& first = nums[0];\ncout << first;', '在可能改变容量的操作之后重新获取引用。', [
   f(['10','20','30'], '假设当前 size=capacity=3，引用 first 指向第 0 项。', [0]),
   f(['10','20','30','40'], 'push_back 后需要扩容，元素被搬到新存储；新数组的第 0 项仍是 10。', [3]),
   f(['10','20','30','40'], '出错：旧引用指向已释放的旧存储，读取它是未定义行为。应重新取得引用。', [0], warning=True)])],
 '1.1': [
  ('中点排除后边界没有前进', '有序数组 [1,3,5] 中查找 5，采用闭区间。', 'if (nums[mid] < target) left = mid;', 'if (nums[mid] < target) left = mid + 1;', 'mid 已经检查过，下一次必须排除它。', [
   f([1,3,5], '初始区间 [0,2]，mid=1，nums[mid]=3 小于 5。', [1], {'left':0,'mid':1,'right':2}),
   f([1,3,5], '错误更新 left=mid，区间变为 [1,2]。', [1], {'left':1,'mid':1,'right':2}),
   f([1,3,5], '出错：mid 仍为 1，再执行同样更新，区间不再变化，陷入循环。', [1], {'left':1,'mid':1,'right':2}, True)]),
  ('在无序数组上直接二分', '在 [8,2,6] 查找 8。', 'binary_search(nums.begin(), nums.end(), 8); // nums 无序', 'sort(nums.begin(), nums.end());\nbool found = binary_search(nums.begin(), nums.end(), 8);', '二分排除半边依赖有序性；排序会改变下标。', [
   f([8,2,6], '目标 8，数组没有按升序排列。', pointers={'left':0,'right':2}),
   f([8,2,6], '中点为 2；按升序二分规则会排除左半边。', [1], {'left':0,'mid':1,'right':2}),
   f([8,2,6], '出错：目标 8 恰好位于被排除的位置，下次只剩 6，最终误报未找到。', [0], {'left':2,'right':2}, True)])],
 '1.2': [
  ('混用闭区间与半开区间', '长度为 3，半开区间初始 right=3。', 'int right = nums.size();\nwhile (left <= right) { int x = nums[right]; }', 'int right = nums.size();\nwhile (left < right) {\n    int mid = left + (right-left)/2;\n    // 只读取 nums[mid]\n}', '半开区间的右端是边界，不一定是有效下标。', [
   f([1,3,5], '半开区间 [0,3)，右边界 3 不属于区间。', pointers={'left':0}),
   f([1,3,5], '出错：直接读取 nums[right] 即 nums[3]，发生越界。', warning=True),
   f([1,3,5], '正确做法：left < right 时计算 mid=1，只读取区间内部。', [1], {'left':0,'mid':1})]),
  ('插入位置等于长度却继续读取', '在 [1,3,5,6] 中查找 7 的插入位置。', 'return nums[left]; // left 可能等于 size', 'return left; // 返回插入位置', '插入位置允许等于长度，但这个位置没有现存元素。', [
   f([1,3,5,6], '目标 7 大于所有元素，插入位置应在末尾之后。'),
   f([1,3,5,6], '查找结束，left=4，表示末尾之后的位置。'),
   f([1,3,5,6], '出错：nums[4] 越界；应返回位置 4，而不是读取该元素。', warning=True)])],
 '1.3': [
  ('用同一个元素配对两次', '数组只有一个 4，目标为 8；题目要求两个不同位置。', 'while (left <= right) { /* 检查两数之和 */ }', 'while (left < right) { /* 检查两数之和 */ }', 'left 与 right 相等时只有一个元素，不能凑成一对。', [
   f([4], '初始 left=right=0，数组只有一个元素。', [0], {'left':0,'right':0}),
   f([4], '出错：left <= right 成立，错误地把同一个 4 使用两次，得到 8。', [0], {'left':0,'right':0}, True),
   f([4], '使用 left < right 时循环不进入，正确报告不存在两个位置。', [0])]),
  ('返回下标时忘记题目约定', '数组 [2,7,11,15] 中目标为 9；题目要求从 1 开始计数。', 'return {left, right};', 'return {left + 1, right + 1};', '内部下标从 0 开始，提交前要转换为题目要求。', [
   f([2,7,11,15], '找到 2 和 7，内部下标是 0 和 1。', [0,1], {'left':0,'right':1}),
   f([2,7,11,15], '出错：直接返回 [0,1]，与题目从 1 开始的约定不符。', [0,1], warning=True),
   f([2,7,11,15], '正确返回 [1,2]；数值本身和选中的位置没有改变。', [0,1])])],
}

from mistake_scenarios import SCENARIOS
CASES.update(SCENARIOS)
