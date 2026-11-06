from html import escape
from mistake_more import DATA
from course_flow import FLOW
from mistake_rebuilt import CASES as REBUILT

# 小片段用于对照错误和修正，变量沿用对应课程，并非完整可执行程序。
EXAMPLES={
'1.1':('数组 [1,3,5] 查找5；中点3偏小后，错误写法可能反复停在同一位置。','left = mid;','left = mid + 1;','中点已经检查过，下一次应排除它。'),
'1.2':('数组 [1,3,5,6] 插入7，答案是4；4等于长度，不是有效下标。','return nums[left];','return left;','返回插入位置本身，不能读取越界位置。'),
'1.4':('空数组没有第0项，直接读取会越界。','int last = nums[0];','if (nums.empty()) return 0;\nint last = nums[0];','先处理空输入，再读取首个元素。'),
'1.6':('数组 [1,1,1,7]、目标7：只缩一次不能得到最短长度1。','if (sum >= target) { /* 缩一次 */ }','while (sum >= target) {\n    best = min(best, right - left + 1);\n    sum -= nums[left++];\n}','每次满足条件都记录长度，持续收缩到不再满足。'),
'1.7':('字符串 abba：最后的a出现时，左边界已经在2，不能退回1。','left = last[ch] + 1;','left = max(left, last[ch] + 1);','取较大值保证左边界只前进。'),
'3.4':('A的两个邻居都连接D；等出队才标记，D可能被重复加入。','q.push(v); // 出队后才标记','seen[v] = true;\nq.push(v);','发现时标记，再入队。'),
'4.1':('已选择1，递归结束后若没有撤销，后续分支会错误地保留1。','path.push_back(nums[i]);\nvisit(i + 1);','path.push_back(nums[i]);\nvisit(i + 1);\npath.pop_back();','每次选择都对应一次撤销。'),
'4.5':('只有一件重量2、价值3的物品，容量4；正序更新会错误得到6。','for (int c = weight; c <= capacity; ++c)\n    dp[c] = max(dp[c], dp[c-weight] + value);','for (int c = capacity; c >= weight; --c)\n    dp[c] = max(dp[c], dp[c-weight] + value);','倒序保证本件物品最多使用一次。'),
'5.2':('B先以距离4入堆，后来更新为3；旧记录4仍可能被弹出。','auto [cost, u] = heap.top();\nheap.pop(); // 直接处理旧记录','auto [cost, u] = heap.top();\nheap.pop();\nif (cost != distance[u]) continue;','过滤过期堆记录，再扩展邻居。'),
'5.5':('依赖 [a,b] 表示先修b才能学a，边应从b指向a。','graph[a].push_back(b);','graph[b].push_back(a);','箭头从前置任务指向后续任务。'),
'6.4':('节点重连后，其后代仍沿这条树枝到达；只改节点自身会保留过期成本。','parent[node] = new_parent;\ncost[node] = new_cost;','parent[node] = new_parent;\ncost[node] = new_cost;\n// 再遍历 node 的所有后代，按父节点的新成本更新。','完整实现中的队列会继续传播子树成本。'),
}

STEPS={
'1.1':(['1,3,5','目标 5','left=0 right=2'],'中点为3，目标更大，错误地令 left=mid。','left=1 right=2，中点仍为1；继续执行仍是同一状态，进入死循环。'),
'1.2':(['1,3,5,6','目标 7','left=4'],'查找结束，插入位置为4。','错误代码读取 nums[4]，长度为4时下标越界。'),
'1.4':(['空数组 []'],'数组没有任何元素。','错误代码读取 nums[0]，发生越界；正确做法直接返回0。'),
'1.6':(['1,1,1,7','目标 7','当前和 10'],'错误代码只缩一次：移除首个1，窗口长度变为3。','仍然满足条件但不继续收缩，错过长度为1的 [7]。'),
'1.7':(['a','b','b','a'],'处理第二个b后，左边界已经移动到2。','最后的a令 left=0+1=1，左边界后退，错误窗口包含重复的b。'),
'3.4':(['A → B → D','A → C → D'],'先处理B，把D放入队列，但尚未标记。','再处理C，D仍未标记，于是第二次入队。'),
'4.1':(['当前路径 []'],'选择1并探索，返回时没有撤销1。','接下来尝试2时路径变成 [1,2]，无法独立生成 [2]。'),
'4.5':(['容量 0 1 2 3 4','价值 0 0 0 0 0'],'正序处理重量2、价值3的物品：容量2更新为3。','容量4读取刚更新的容量2，得到6；同一物品被使用两次。'),
'5.2':(['A→B=4','A→C=1','C→B=2'],'B先以4入堆，经C改善为3并先处理。','旧记录4随后弹出；未过滤时会重复扩展B。此例不一定产生错误距离，但增加无效工作。'),
'5.5':(['依赖 [a,b]','必须先 b 后 a'],'错误建边 a→b。','拓扑排序可能输出 a、b，违反题意的先修顺序。'),
'6.4':(['新父节点成本 6','节点成本由10降到8','后代边长 2'],'只更新节点的父指针与成本。','后代仍保留旧成本12；正确值应为8+2=10，后续比较会失真。'),
}

def original_frames(id):
    if id in DATA:
        scenario,wrong,right,reason,states=DATA[id]
        return [{'cells':states[:i+1], 'active':[i], 'text':('错误示例：'+scenario if i==0 else states[i])} for i in range(len(states))]
    if id not in STEPS:return []
    cells,first,last=STEPS[id]
    return [{'cells':cells,'active':[],'text':'错误演示：'+first},{'cells':cells,'active':list(range(len(cells))),'text':last}]

def original_code_mistake(id,lesson_target):
    if id in DATA:
        scenario,wrong,right,reason,_=DATA[id]
        return '<div class="mistake-example"><h3>结合例子看错误与纠正（C++）</h3><p>'+escape(scenario)+'</p><strong>容易写错</strong><pre><code>'+escape(wrong)+'</code></pre><strong>修改后</strong><pre><code>'+escape(right)+'</code></pre><p>'+escape(reason)+'</p><p><a class="implementation-button" href="'+escape(lesson_target,quote=True)+'?mistake=1#demo">查看错误过程演示 →</a></p><p class="muted">以上是局部示意；完整可运行程序见上方语言选项。</p></div>'
    if id not in EXAMPLES:return ''
    scenario,wrong,right,reason=EXAMPLES[id]
    return '<div class="mistake-example"><h3>结合例子看错误与纠正（C++）</h3><p>'+escape(scenario)+'</p><strong>容易写错</strong><pre><code>'+escape(wrong)+'</code></pre><strong>修改后</strong><pre><code>'+escape(right)+'</code></pre><p>'+escape(reason)+'</p><p><a class="implementation-button" href="'+escape(lesson_target,quote=True)+'?mistake=1#demo">查看错误过程演示 →</a></p><p class="muted">以上是突出问题的局部片段；完整可运行程序见上方语言选项。</p></div>'


def mistake_frames(id):
    if id in REBUILT:
        return [{'name': case[0], 'frames': case[5]} for case in REBUILT[id]]
    if id == '1.5':
        def arr(values,text,active=(),pointers=None,warning=False):
            return {'cells':[str(v) for v in values], 'text':text,'active':active,'indexed':True,'pointers':pointers or {},'warning':warning}
        return [
          {'name':'删除后跳过前移元素','frames':[
            arr([3,3,2],'从左向右删除3，先检查下标0。',[0],{'i':0}),
            arr([3,2],'删除首个3，原下标1的3前移到下标0。',[0],{'i':0}),
            arr([3,2],'⚠ 即将出错：循环把i加到1，跳过了前移的3。',[0,1],{'i':1},True),
            arr([3,2],'检查下标1的2后结束，错误地留下一个3。',[0],{'i':1},True)]},
          {'name':'把移除当成去重','frames':[
            arr([2,2,4],'目标值为3；数组里的2、2、4都应保留。',[0],{'fast':0}),
            arr([2,2,4],'第一个2与目标3不同，保留。',[0],{'fast':0,'slow':0}),
            arr([2,2,4],'⚠ 即将出错：第二个2与前一个相同，但它不是目标值，不能丢掉。',[1],{'fast':1},True),
            arr([2,2,4],'错误去重仅得到 [2,4]；正确结果前缀应为 [2,2,4]，长度3。',[0,1],warning=True)]},
        ]
    if id == '5.3':
        weighted={'nodes':[['S',60,150],['A',205,55],['T',355,150]],'edges':[[0,2,10],[0,1,1],[1,2,1]],'directed':True}
        def frame(network,text,cells,highlight=(),route=(),warning=False):
            return {'network':network,'text':text,'cells':cells,'active':[], 'highlight':highlight,'route':route,'warning':warning}
        return [
          {'name':'八方向却用曼哈顿距离','frames':[
            {'cells':[],'active':[],'grid':['..','..'],'start':[0,0],'goal':[1,1],'current':[0,0],
             'scores':{'0,0':{'g':0,'h':2,'f':2}},'scoreKind':'astar',
             'text':'S=(0,0)，T=(1,1)。此固定例子允许八方向移动，每一步（含斜向）代价均为 1。'},
            {'cells':[],'active':[],'grid':['..','..'],'start':[0,0],'goal':[1,1],'route':[[0,0],[1,1]],
             'distances':{'0,0':0,'1,1':1},'parents':{'1,1':'0,0'},
             'text':'实际沿对角线走一步就到 T，所以从 S 到 T 的最短代价为 1。'},
            {'cells':[],'active':[],'grid':['..','..'],'start':[0,0],'goal':[1,1],'current':[0,0],
             'scores':{'0,0':{'g':0,'h':2,'f':2}},'scoreKind':'astar','warning':True,
             'text':'出错：曼哈顿 h=1+1=2，大于真实剩余代价 1，破坏了启发式下界。'},
            {'cells':[],'active':[],'grid':['..','..'],'start':[0,0],'goal':[1,1],'route':[[0,0],[1,1]],
             'scores':{'0,0':{'g':0,'h':1,'f':1},'1,1':{'g':1,'h':0,'f':1}},'parents':{'1,1':'0,0'},'scoreKind':'astar',
             'text':'换用切比雪夫 h=max(1,1)=1，与本例移动规则匹配。'}]},
          {'name':'首次发现终点就停止','frames':[
            frame(weighted,'使用 h=0，图上的数字是边代价；起点S到终点T。',['S:0','A:∞','T:∞'],[0]),
            frame(weighted,'扩展S，发现直达T代价10，同时发现A代价1。',['待处理 A:1','待处理 T:10'],[0]),
            frame(weighted,'⚠ 即将出错：若发现T就立刻返回，会返回代价10，但A还在队列里。',['错误返回：10','A仍待处理：1'],[0,2],warning=True),
            frame(weighted,'先弹出A并松弛A→T，T的距离从10改善为2。',['A:1','T:2'],[1,2]),
            frame(weighted,'有效距离2的T出队后结束，恢复最短路径 S→A→T。',['正确代价：2'],[2],[0,1,2])]},
        ]
    result=[{'name':'代码对照示例','frames':original_frames(id)}]
    for title,example,correction in FLOW[id][4]:
        result.append({'name':title,'frames':[{'cells':[example],'active':[0],'text':'反例：'+example},{'cells':[example,correction],'active':[1],'text':'纠正：'+correction}]})
    return result

def code_mistakes(id,lesson_target):
    if id in REBUILT:
        result = ''
        for index, (title, scenario, wrong, right, reason, frames) in enumerate(REBUILT[id], 1):
            url = escape(lesson_target, quote=True) + '?mistake=' + str(index) + '#demo'
            result += ('<div class="mistake-example"><h3>' + escape(title) + '</h3><p>' + escape(scenario)
                       + '</p><strong>容易写错</strong><pre><code>' + escape(wrong)
                       + '</code></pre><strong>修改后</strong><pre><code>' + escape(right)
                       + '</code></pre><p>' + escape(reason) + '</p><a class="implementation-button" href="'
                       + url + '">查看此错误的过程演示 →</a></div>')
        return result
    if id == '1.5':
        cases=[
          ('边遍历边删除导致漏检','从 [3,3,2] 中移除3；删除首个元素后，下一个3会前移。','for (int i = 0; i < nums.size(); ++i)\n    if (nums[i] == val) nums.erase(nums.begin() + i);','int slow = 0;\nfor (int fast = 0; fast < nums.size(); ++fast)\n    if (nums[fast] != val) nums[slow++] = nums[fast];','错误循环删除后仍递增下标，跳过前移元素；覆盖法只复制要保留的值。'),
          ('把移除目标值和去重混淆','从 [2,2,4] 中移除3，两个2都必须保留。','if (fast == 0 || nums[fast] != nums[fast-1])\n    nums[slow++] = nums[fast];','if (nums[fast] != val)\n    nums[slow++] = nums[fast];','去重检查相邻值；移除元素只检查是否等于目标值。')]
        return ''.join('<div class="mistake-example"><h3>'+escape(title)+'</h3><p>'+escape(scenario)+'</p><strong>错误写法</strong><pre><code>'+escape(wrong)+'</code></pre><strong>纠正后</strong><pre><code>'+escape(right)+'</code></pre><p>'+escape(reason)+'</p><a class="implementation-button" href="'+escape(lesson_target,quote=True)+'?mistake='+str(index)+'#demo">查看逐步演示 →</a></div>' for index,(title,scenario,wrong,right,reason) in enumerate(cases,1))
    if id == '5.3':
        cases=[
          ('八方向移动却使用曼哈顿距离','允许斜向一步且代价为1，S=(0,0)、T=(1,1)：真实最短代价是1，曼哈顿估计为2。','int h = abs(r - tr) + abs(c - tc);','int h = max(abs(r - tr), abs(c - tc));','每个方向一步代价均为1时，切比雪夫距离是下界。若对角代价为√2，应采用与代价匹配的八方向估计。'),
          ('首次发现终点就停止','S→T代价10，S→A和A→T各代价1；使用h=0的A*，首次发现T时还有更短路线待探索。','if (v == goal) return reconstruct(parent, v); // 生成邻居时提前返回','// 从优先队列取出有效状态后判断终点\nif (cost != distance[u]) continue;\nif (u == goal) return reconstruct(parent, u);','此处 h=0；一般A*使用适当的启发式及正确的重复状态处理。仅在当前有效的目标状态出队时终止。')]
        result=''
        for index,(title,scenario,wrong,right,reason) in enumerate(cases,1):
            url=escape(lesson_target,quote=True)+'?mistake='+str(index)+'#demo'
            result+='<div class="mistake-example"><h3>'+escape(title)+'</h3><p>'+escape(scenario)+'</p><strong>容易写错</strong><pre><code>'+escape(wrong)+'</code></pre><strong>修改后</strong><pre><code>'+escape(right)+'</code></pre><p>'+escape(reason)+'</p><a class="implementation-button" href="'+url+'">查看此错误的逐步演示 →</a></div>'
        return result
    result=original_code_mistake(id,lesson_target)
    for index,(title,example,correction) in enumerate(FLOW[id][4],1):
        url=escape(lesson_target,quote=True)+'?mistake='+str(index+1)+'#demo'
        result+='<div class="mistake-example"><h3>'+escape(title)+'</h3><p><strong>具体反例：</strong>'+escape(example)+'</p><p><strong>纠正方法：</strong>'+escape(correction)+'</p><p><a class="implementation-button" href="'+url+'">查看此错误的示意 →</a></p></div>'
    return result
