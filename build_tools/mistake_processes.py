"""Concrete, deterministic teaching traces. No undefined result is fabricated."""
from copy import deepcopy


def frame(text, warning=False, **data):
    return dict(cells=[], active=[], text=text, warning=warning, **data)


def array(values, text, active=(), pointers=None, warning=False):
    return dict(cells=list(map(str, values)), indexed=True, active=list(active),
                pointers=pointers or {}, text=text, warning=warning)


def boxes(text, groups, warning=False, **data):
    return frame(text, warning, containers=[dict(name=n, values=v) for n, v in groups], **data)


def net(labels, edges, text, current=(), meta=None, chosen=(), warning=False, directed=True):
    # Generous vertical spacing leaves room for two metadata lines per node.
    layouts={2:[(100,110),(350,110)],3:[(220,40),(80,210),(360,210)],
             4:[(220,35),(85,150),(350,150),(220,285)],
             5:[(220,35),(80,140),(350,140),(80,275),(350,275)],
             7:[(220,35),(110,150),(340,150),(45,275),(175,275),(305,275),(435,275)]}
    positions=layouts[len(labels)]
    return frame(text, warning, network=dict(nodes=[[n,*p] for n,p in zip(labels,positions)],
                 edges=edges, directed=directed), highlight=list(current),
                 nodeNotes=meta or {}, chosenEdges=list(chosen))


def grid(rows, start, goal, text, route=(), current=None, warning=False, **data):
    return frame(text, warning, grid=rows, start=start, goal=goal, route=list(route),
                 current=current, **data)


def rebuild(cases):
    def put(key, index, frames):
        old=cases[key][index]
        cases[key][index]=(*old[:5],frames)

    # Counting work: every square is an actual invocation, not an asymptotic claim.
    work=[]
    for i in range(4):
        for j in range(3):
            work.append(frame(f'i={i}, j={j}：执行 work，第 {len(work)+1} 次。',
                              work=dict(rows=4, cols=3, done=len(work)+1)))
    work += [frame('出错：把两层循环直接认成 n²=16；图中实际只有 4×3=12 次。',True,
                   work=dict(rows=4,cols=3,done=12)),
             frame('内层固定 3 次，工作量为 3n，因此为 O(n)。',work=dict(rows=4,cols=3,done=12))]
    put('0.1',0,work)
    put('0.1',1,[frame('同样处理 1000 个元素，先比较同一机器的增长趋势。',bars=[['甲 n=1000',2],['甲 n=2000',4]],barUnit='ms'),
        frame('机器乙执行同一算法：耗时可不同，工作量仍随 n 线性增长。',bars=[['甲 n=1000',2],['乙 n=1000',5]],barUnit='ms'),
        frame('出错：O(n) 没有秒这个单位，不能据此推断要运行 1000 秒。',True,bars=[['甲 n=1000',2],['乙 n=1000',5]],barUnit='ms')])
    put('0.3',0,[boxes('初始哈希表只有键 4；查询键 99。',[('哈希表',['4 → 10'])]),
        boxes('operator[] 查找 99，未找到时会创建默认值 0。',[('哈希表',['4 → 10','99 → 0'])],True),
        boxes('改用 find(99)：返回 end，表仍保持原来的内容。',[('哈希表',['4 → 10']),('查询结果',['99 不存在'])])])
    put('0.3',1,[boxes('依次插入 3、1、2；桶位置不等于键的大小顺序。',[('桶 0',['3']),('桶 1',['1']),('桶 2',['2'])]),
        boxes('一次可能的遍历依次读出 2、3、1。此顺序仅作示意。',[('可能输出',['2','3','1'])]),
        boxes('出错：输出不是升序；unordered_map 不承诺有序。',[('可能输出',['2','3','1'])],True),
        boxes('先收集键再排序，输出 1、2、3。',[('排序后的键',['1','2','3'])])])
    put('0.4',0,[boxes('栈中只有一个元素，右端是栈顶。',[('栈（右端栈顶）',['3'])]),
        boxes('pop() 移除栈顶后栈为空。',[('栈（右端栈顶）',[])]),
        boxes('出错：空栈上调用 top() 是未定义行为；不会演示一个虚构的返回值。',[('栈（右端栈顶）',[])],True),
        boxes('先检查 empty()，为空就跳过读取。',[('栈（右端栈顶）',[])])])
    put('0.4',1,[array(list('ABCD'),'初始列表，准备删除下标 0。',[0]),
        array(list('BCD'),'删除 A 后，B、C、D 各向左搬移一次。',[0,1,2]),
        array(list('CD'),'再删除 B，还要搬移 C、D。累计搬移 3+2=5 次。',[0,1],warning=True),
        boxes('deque 的 popleft 从队头移除，不需要整体搬移。',[('deque 队头 → 队尾',list('BCD'))])])
    heap=[[0,1],[0,2]]
    put('0.5',0,[net(['8','3','6'],heap,'插入 8、3、6，默认最大堆保持父节点不小于子节点。',meta={0:['top = 8']}),
        net(['8','3','6'],heap,'出错：读取 top 得到 8，目标却是最小值 3。',[0],warning=True),
        net(['3','8','6'],heap,'使用 greater 构造最小堆，top 才为 3。',[0],{0:['top = 3']})])
    put('0.5',1,[net(['1','3','2'],heap,'最小堆仅要求父节点不大于孩子；兄弟 3、2 不要求有序。'),
        array([1,3,2],'按底层数组依次读取。',[0]),array([1,3,2],'出错：读到 3 后再读 2，不是升序。',[1,2],warning=True),
        boxes('依次 top/pop 才得到排序输出。',[('输出',[1,2,3])])])
    put('1.4',0,[array([1,1,2,2,3],'原数组，开始原地去重。',pointers={'slow':0,'fast':1}),
        array([1,2,2,2,3],'读到 2，将它写到有效前缀。',[1],{'slow':1,'fast':2}),
        array([1,2,3,2,3],'写入 3，返回 k=3。前三项就是答案。',[0,1,2],{'k':3}),
        array([1,2,3,2,3],'出错：因为尾部仍有 2、3 就判失败；题目只检查前 k 项。',[3,4],warning=True)])
    put('1.4',1,[array([],'空数组 size=0，没有合法下标。'),array([],'出错：读取 nums[0] 越界。',pointers={'last':0},warning=True),array([],'先检查 empty()，返回 k=0。')])
    put('2.3',1,[net(['A:1','B:1'],[],'两个对象都存储值 1，但身份分别为 A、B。',meta={0:['地址 α'],1:['地址 β']}),
        net(['A:1','B:1'],[],'比较 a.val == b.val，结果为 true。',[0,1],{0:['值 1'],1:['值 1']}),
        net(['A:1','B:1'],[],'出错：值相同不能证明同一对象；a != b。',[0,1],{0:['地址 α'],1:['地址 β']},warning=True)])
    put('2.4',0,[net(['A','B'],[[0,1]],'错误存储只加入 A→B；尝试从 B 出发。',[1],{0:['邻居 B'],1:['邻居 ∅']}),
        net(['A','B'],[[0,1]],'出错：B 的邻接表为空，遗漏无向边的反向可达性。',[1],{1:['查找 A 失败']},warning=True),
        net(['A','B'],[[0,1],[1,0]],'同时存储 A→B 与 B→A。',[1],{0:['邻居 B'],1:['邻居 A']},[[1,0]])])
    put('2.5',1,[net(['0','1','2'],[[0,1]],'有 3 个节点，只有 1 条边。',directed=False),
        array(['邻居列表'],'错误按 edgeCount=1 创建外层数组。'),
        array(['邻居列表'],'出错：访问 graph[2] 越界，节点 2 也必须有自己的列表。',pointers={'访问':2},warning=True),
        array(['[1]','[0]','[]'],'应按 nodeCount=3 创建外层数组。',[2])])
    put('3.1',1,[net(['A','B'],[[0,1],[1,0]],'进入 A，未标记。',[0],{0:['调用栈 A']}),
        net(['A','B'],[[0,1],[1,0]],'从 A 递归进入 B。',[1],{1:['调用栈 A,B']},[[0,1]]),
        net(['A','B'],[[0,1],[1,0]],'出错：B 又进入 A，栈 A,B,A，随后会持续重复。',[0],{0:['重复进入 A']},[[1,0]],True),
        net(['A','B'],[[0,1],[1,0]],'进入时标记 seen；B 遇到已访问的 A 时跳过。',[1],{0:['seen=true'],1:['seen=true']})])
    put('3.2',0,[boxes('空栈，依次压入 B、C。',[('栈：右端栈顶',[])]),boxes('push(B)。',[('栈：右端栈顶',['B'])]),
        boxes('push(C)，C 现在位于栈顶。',[('栈：右端栈顶',['B','C'])]),boxes('出错：pop 首先得到 C，而不是预期的 B。',[('栈：右端栈顶',['B']),('刚访问',['C'])],True),
        boxes('希望先访问 B，则先压 C 再压 B。',[('栈：右端栈顶',['C','B'])])])
    diamond=[[0,1],[0,2],[1,3],[2,3]]
    # Show a valid LIFO schedule: A pushes B then C; C pushes D while B is
    # still pending. B can add D again after D was processed without a guard.
    put('3.2',1,[net(['A','B','C','D'],diamond,'弹出 A，压入 B、C；右端为栈顶。',[0],{1:['栈中'],2:['栈顶'],3:['未标记']}),
        boxes('弹出 C，加入 D。',[('栈：右端栈顶',['B','D'])]),boxes('弹出 D 并处理，再弹出 B。',[('栈：右端栈顶',[]),('已处理',['A','C','D','B'])]),
        boxes('出错：邻居入栈时不检查标记，B 又将已处理的 D 入栈，产生重复工作。',[('栈：右端栈顶',['D'])],True),
        boxes('首次入栈就标记，并在入栈前检查 seen，可跳过重复的 D。',[('栈：右端栈顶',[])])])
    # Replace the scenario/code too: the old "both pending before D pops" claim
    # does not match a simple LIFO DFS on this diamond.
    old=cases['3.2'][1]
    cases['3.2'][1]=(old[0],'A 连接 B、C；B、C 都连接 D，入栈前没有检查标记。',
        'st.push(v); // 不检查 seen，可能重复处理',old[3],
        '此例先处理 C、D，再处理 B；B 若无条件加入 D 就会重复。若出栈检查可避免重复扩展。',old[5])
    for key,index,initial,after,good in [('3.3',1,['A','B'],['A'],['A','B']),('3.5',1,['A'],[],['A'])]:
        put(key,index,[boxes('当前列表尚未保存。',[('原列表',initial),('结果',[])]),
            boxes('append 保存的是同一列表的引用。',[('原列表 · 对象 L',initial),('结果[0] → 对象 L',initial)]),
            boxes('出错：修改原列表后，结果中的内容跟着改变。',[('原列表 · 对象 L',after),('结果[0] → 对象 L',after)],True),
            boxes('保存 copy() 后两个对象独立，已保存结果保持原值。',[('原列表 · 对象 L',after),('结果[0] → 副本',good)])])
    put('3.5',0,[net(['A','B','C','D','E'],[[0,1],[0,2],[1,3],[1,4]],'本层队列 [B,C]，本层应固定处理两个节点。',[1,2]),
        boxes('i=0：处理 B，D、E 入队，队列长度从 2 变成 3。',[('队头 → 队尾',['C','D','E']),('本层已输出',['B'])]),
        boxes('i=1：处理 C，队列剩 [D,E]，长度变成 2。',[('队头 → 队尾',['D','E']),('本层已输出',['B','C'])]),
        boxes('此例 i=2 时 2<2 为假，恰好没有混层，但动态边界仍不可靠。',[('队头 → 队尾',['D','E'])]),
        boxes('反例：若 B 有 D、E，C 有 F、G，处理 C 后 size=4，i=2 仍成立，错误处理下一层 D。',[('队头 → 队尾',['E','F','G']),('错误的本层',['B','C','D'])],True),
        boxes('正确做法：进入本层前固定 width=2，只处理 B、C。',[('下一层队列',['D','E','F','G'])])])
    old=cases['3.5'][0]
    cases['3.5'][0]=(old[0],'本层 [B,C]；对比仅 B 有两个孩子，以及 B、C 各有两个孩子的情况。',*old[2:5],old[5])
    rows=['...','...'];s=[0,0];t=[0,2]
    put('3.7',0,[grid(rows,[0,1],[1,2],'当前位置 (0,1)，下一步试探上方。',current=[0,1]),
        grid(rows,[0,1],[1,2],'候选 (-1,1) 位于地图之外。',current=[0,1],probe=[-1,1]),
        grid(rows,[0,1],[1,2],'出错：C++ 先读取 grid[-1][1] 会越界；Python 负索引则会误读末行。',current=[0,1],warning=True,probe=[-1,1]),
        grid(rows,[0,1],[1,2],'先判断行号 >=0，条件为假，跳过访问。',current=[0,1],probe=[-1,1])])
    long=[[0,0],[1,0],[1,1],[1,2],[0,2]]
    short=[[0,0],[0,1],[0,2]]
    put('3.7',1,[grid(rows,s,t,'从 S 开始，DFS 的邻居顺序先向下。',route=[s],current=s),
        *[grid(rows,s,t,f'DFS 进入 {p}，当前深度 {i}。',route=long[:i+1],current=p,
               distances={','.join(map(str,q)):j for j,q in enumerate(long[:i+1])}) for i,p in enumerate(long[1:],1)],
        grid(rows,s,t,'出错：把首次找到的 4 步路径当作最短；上方还有 2 步路径。',route=long,warning=True),
        grid(rows,s,t,'BFS 按距离扩展，最短路径为 2 步。',route=short,distances={'0,0':0,'0,1':1,'0,2':2},parents={'0,1':'0,0','0,2':'0,1'})])
    put('3.8',1,[grid(['..','..'],[0,0],[1,1],'只允许上下左右，从 S 出发。',route=[[0,0]]),
        grid(['..','..'],[0,0],[1,1],'出错：加入对角方向会得到非法的一步路径。',route=[[0,0],[1,1]],warning=True),
        grid(['..','..'],[0,0],[1,1],'合法路径先向右一步。',route=[[0,0],[0,1]],current=[0,1]),
        grid(['..','..'],[0,0],[1,1],'再向下一步，到达 T，共 2 步。',route=[[0,0],[0,1],[1,1]],parents={'0,1':'0,0','1,1':'0,1'},distances={'0,0':0,'0,1':1,'1,1':2})])
    for index,all_intervals,choices in [(0,[[0,3],[3,6],[2,4]],[[],[[2,4]],[[0,3],[3,6]]]),(1,[[0,1],[1,2],[0,2]],[[],[[0,1],[1,2]],[[0,2]]])]:
        texts=[f['text'] for f in cases['4.2'][index][5]]
        put('4.2',index,[frame(text,j==1,intervals=dict(all=all_intervals,chosen=choices[j],current=-1),
                        intervalValues=([1,1,10] if index else [3,3,2])) for j,text in enumerate(texts)])
    put('4.3',0,[array([4,1,3,2],'原数组，拆分为两段。'),array([1,4,3,2],'左段排序完成。',[0,1]),
        array([1,4,2,3],'右段排序完成，仍须合并。',[2,3]),array([1,4,2,3],'出错：直接拼接得到 1,4,2,3；4>2。',[1,2],warning=True),
        boxes('合并：比较左右段头部，依次取 1、2、3、4。',[('左段',[1,4]),('右段',[2,3]),('合并输出',[1,2,3,4])])])
    put('4.3',1,[array([1,3,5,7],'left 初始列表。'),array([3,5,7],'pop(0) 取出 1，剩余 3 项前移。',[0,1,2]),
        array([5,7],'再次头删，2 项前移；反复头删可能导致二次方搬移成本。',[0,1],warning=True),array([1,3,5,7],'改用下标 i 读取，原列表不动。',pointers={'i':2})])
    put('4.4',0,[array([0,1,'?'],'错误初始化 dp[0]=0、dp[1]=1。',[0,1]),
        array([0,1,1],'计算 dp[2]=dp[1]+dp[0]=1。',[2]),array([0,1,1],'出错：少算直接跨两级的方案；实际有 1+1 与 2。',[2],warning=True),
        array([1,1,2],'修正 dp[0]=1，得到 dp[2]=2。',[0,2])])
    put('4.4',1,[array([1134903170,1836311903],'计算下一项前，两个加数都能用 int32 表示。'),
        frame('数学和为 2971215073，超过 int32 最大值。',bars=[['int32 上限',2147483647],['下一项',2971215073]],barUnit=''),
        frame('出错：有符号加法溢出属于未定义行为；不能假设一定回绕为负数。',True,bars=[['int32 上限',2147483647],['下一项',2971215073]],barUnit=''),
        array([1836311903,2971215073],'在本例使用 long long，并继续检查后续输入范围。',[1])])
    put('4.6',1,[array(['a'],'字符串长度为 1，前缀长度 i=1。',pointers={'i':1}),
        array(['a'],'出错：s[1] 是终止字符位置，不是前缀的最后一个字符；继续写入或越过它另有风险。',pointers={'i':1},warning=True),
        array(['a'],'访问 s[i-1] 即 s[0]，得到 a。',[0],{'i-1':0})])
    # C++ std::string[size()] is readable as the null character, not itself UB.
    old=cases['4.6'][1];cases['4.6'][1]=(*old[:4],'前缀长度 1 的末字符在下标 0；C++ s[size()] 读到终止字符，不能当作有效字符。',old[5])
    put('5.2',1,[boxes('B 被发现两次，距离表已经更新为 3。',[('小根堆：按距离出堆',['(3,B)','(4,B)']),('dist[B]',['3'])]),
        boxes('先弹出 (3,B)，与 dist[B] 一致，可以扩展。',[('堆',['(4,B)']),('dist[B]',['3'])]),
        boxes('出错：再弹出 (4,B) 仍去扩展，同一个节点做了重复工作。',[('刚弹出',['(4,B)']),('dist[B]',['3'])],True),
        boxes('检查 4 != dist[B]，跳过这条过期记录。',[('堆',[]),('dist[B]',['3'])])])
    path_edges=[[0,3,1],[3,2,1],[2,1,1]]
    put('5.4',0,[net(['0','1','2','3'],path_edges,'初始只知道三条直接边。',meta={0:['d(0,1)=∞','d(0,2)=∞']}),
        net(['0','1','2','3'],path_edges,'错误 i,j,k 顺序：先处理 (0,1)，此时 d(0,2)=∞。',[0,1],{0:['候选仍是 ∞']}),
        net(['0','1','2','3'],path_edges,'随后 (0,2) 才通过 3 更新为 2。',[0,2],{0:['d(0,2)=2']},[[0,3],[3,2]]),
        net(['0','1','2','3'],path_edges,'出错：不会回头重算 (0,1)，仍保留 ∞，漏掉可达路径。',[1],{0:['d(0,1)=∞，错误']},warning=True),
        net(['0','1','2','3'],path_edges,'以 k 为外层，允许中转点 3 后，得到 0→3→2→1，距离 3。',[0,1],{0:['d(0,1)=3']},[[0,3],[3,2],[2,1]])])
    put('5.5',1,[net(['A','B','C'],[[0,1],[1,0]],'初始入度 A=1、B=1、C=0；只有 C 入队。',[2],{0:['入度 1'],1:['入度 1'],2:['入度 0']}),
        net(['A','B','C'],[[0,1],[1,0]],'输出 C，队列空；A、B 仍互相等待。',[2],{0:['未处理'],1:['未处理'],2:['已输出']}),
        net(['A','B','C'],[[0,1],[1,0]],'出错：只输出 1/3 个节点就宣布成功；环中的节点没有被处理。',[0,1],{0:['入度 1'],1:['入度 1']},warning=True),
        net(['A','B','C'],[[0,1],[1,0]],'检查 order.size()!=n，报告 A↔B 存在环。',[0,1],chosen=[[0,1],[1,0]])])
    put('5.6',0,[net(['A','B','C'],[[1,0]],'父指针 B→A；C 是独立的根。',meta={0:['root A'],1:['parent A'],2:['root C']}),
        net(['A','B','C'],[[1,2]],'出错：直接改 parent[B]=C，把 B 从 A 的集合拆开。',[1],{0:['find(A)=A'],1:['find(B)=C']},[[1,2]],True),
        net(['A','B','C'],[[1,0],[0,2]],'先找根 find(B)=A，再将 parent[A] 指向 C。',[0],{0:['parent C'],1:['parent A'],2:['root C']},[[0,2]])])
    subset_edges=[[0,1],[0,2],[1,3]]
    put('4.1',0,[net(['∅','A','B','AB'],subset_edges,'进入根节点，当前选择为空。',[0],{0:['path=[]','尚未记录'],1:['未探索'],2:['未探索'],3:['未探索']}),
        net(['∅','A','B','AB'],subset_edges,'出错：if (!path.empty()) 跳过了根的空集；漏解在此发生。',[0],{0:['漏记 []']},warning=True),
        net(['∅','A','B','AB'],subset_edges,'选择 A，记录 [A]。',[1],{0:['未记录'],1:['path=[A]','已记录']},[[0,1]]),
        net(['∅','A','B','AB'],subset_edges,'选择 B，记录 [A,B]，然后回溯。',[3],{3:['path=[A,B]','已记录']},[[0,1],[1,3]]),
        net(['∅','A','B','AB'],subset_edges,'回到根再选择 B，记录 [B]；只有 3 种。',[2],{0:['漏记 []'],1:['已记录'],2:['已记录'],3:['已记录']},[[0,2]]),
        net(['∅','A','B','AB'],subset_edges,'修正：进入每个节点都记录当前 path，包括根 []，共 4 种。',[0],{0:['记录 []'],1:['记录 [A]'],2:['记录 [B]'],3:['记录 [A,B]']})])
    put('4.1',1,[net(['∅','A','B','AB'],subset_edges,'根节点 path=[]，先探索 A 分支。',[0],{0:['path=[]']}),
        net(['∅','A','B','AB'],subset_edges,'push A；当前路径 [A]。',[1],{1:['path=[A]']},[[0,1]]),
        net(['∅','A','B','AB'],subset_edges,'A 分支返回，本应 pop A，但遗漏了撤销。',[0],{0:['path 仍为 [A]']},[[0,1]]),
        net(['∅','A','B','AB'],subset_edges,'出错：从根尝试 B，却得到 [A,B]，没有得到独立的 [B]。',[2],{2:['预期 [B]','实际 [A,B]']},[[0,2]],True),
        net(['∅','A','B','AB'],subset_edges,'修正：返回时 pop A，再选择 B，path=[B]。',[2],{0:['撤销后 []'],2:['path=[B]']},[[0,2]])])
    # A complete topology remains on screen; only the active branch changes.
    long_edges=[[0,1],[1,2],[2,3],[0,4],[4,3]]
    put('3.1',0,[net(['A','B','C','T','D'],long_edges,'从 A 开始；邻居先处理 B。',[0],{0:['深度 0']}),
        net(['A','B','C','T','D'],long_edges,'进入 B，记录前驱 A。',[1],{1:['深度 1','来自 A']},[[0,1]]),
        net(['A','B','C','T','D'],long_edges,'进入 C，记录前驱 B。',[2],{2:['深度 2','来自 B']},[[0,1],[1,2]]),
        net(['A','B','C','T','D'],long_edges,'首次进入 T，沿 A→B→C→T 走了 3 步。',[3],{3:['深度 3','来自 C']},[[0,1],[1,2],[2,3]]),
        net(['A','B','C','T','D'],long_edges,'出错：首次找到不保证最短，另一条 A→D→T 只有 2 步。',[3],{3:['DFS 首条 3 步','最短 2 步']},[[0,4],[4,3]],True)])
    duplicate=[]
    for text,current,queue,meta,chosen,warn in [
        ('初始化：只将 A 入队。',[0],['A'],{0:['d=0','已入队，未标记']},[],False),
        ('A 出队，发现 B、C；错误写法入队时不做标记。',[0],['B','C'],{0:['d=0，已访问'],1:['d=1，来自 A'],2:['d=1，来自 A'],3:['未发现']},[[0,1],[0,2]],False),
        ('B 出队，D 首次入队，但 seen[D] 仍为 false。',[1],['C','D'],{1:['已访问'],2:['待处理'],3:['d=2，来自 B','seen=false']},[[1,3]],False),
        ('C 出队，同样看到 seen[D]=false。',[2],['D'],{2:['已访问'],3:['队列中，未标记']},[[2,3]],False),
        ('出错：C 又把 D 加入队列，两个待处理条目都指向同一个节点 D。',[3],['D','D'],{3:['重复入队 ×2','seen=false']},[[1,3],[2,3]],True),
        ('正确写法：首次将 D 入队就标记；C 发现 D 时跳过。',[3],['D'],{3:['seen=true','来自 B，d=2']},[[1,3]],False)]:
        f=net(['A','B','C','D'],diamond,text,current,meta,chosen,warn)
        f['containers']=[dict(name='队头 → 队尾（每格是一个待处理条目）',values=queue)]
        duplicate.append(f)
    put('2.6',0,deepcopy(duplicate));put('3.4',1,deepcopy(duplicate))
    for lesson in ('2.6','3.3'):
        index=1 if lesson=='2.6' else 0
        put(lesson,index,[net(['A','B','C','D'],diamond,'当前路径 A→B→D，记录第一条结果。',[3],{0:['onPath=true'],1:['onPath=true'],3:['onPath=true']},[[0,1],[1,3]]),
            net(['A','B','C','D'],diamond,'从 D、B 回溯到 A，却没有撤销永久 visited[D]。',[0],{1:['仍标记'],3:['仍标记']}),
            net(['A','B','C','D'],diamond,'进入 C，准备尝试 C→D。',[2],{2:['当前路径 A,C'],3:['visited=true']},[[0,2]]),
            net(['A','B','C','D'],diamond,'出错：D 被永久标记，第二条合法路径 A→C→D 被漏掉。',[3],{3:['错误跳过']},[[2,3]],True),
            net(['A','B','C','D'],diamond,'正确做法：回溯时撤销路径标记，此分支可以再次选择 D。',[3],{0:['onPath=true'],2:['onPath=true'],3:['重新进入']},[[0,2],[2,3]])])
    route_edges=[[0,1],[0,2],[1,3]]
    put('3.6',0,[net(['S','B','C','T'],route_edges,'初始化从 S 出发；访问顺序并不等于路径。',[0],{0:['d=0'],1:['未发现'],2:['未发现'],3:['未发现']}),
        net(['S','B','C','T'],route_edges,'处理 S，B、C 入队，同时记录各自前驱。',[0],{1:['d=1，来自 S'],2:['d=1，来自 S']}),
        net(['S','B','C','T'],route_edges,'处理 B，发现 T；T 的前驱为 B。',[1],{3:['d=2，来自 B']},[[1,3]]),
        net(['S','B','C','T'],route_edges,'随后处理 C、T，访问次序为 S,B,C,T。',[2,3],{1:['来自 S'],2:['来自 S'],3:['来自 B']}),
        net(['S','B','C','T'],route_edges,'出错：访问次序中 B→C 没有边，不能把它当作连续路径。',[1,2],{1:['B 与 C 不相邻'],2:['B 与 C 不相邻']},warning=True),
        net(['S','B','C','T'],route_edges,'从 T 沿前驱回溯 T←B←S，反转得到 S→B→T。',[0,1,3],{0:['起点'],1:['来自 S'],2:['不在结果路径'],3:['来自 B']},[[0,1],[1,3]])])
    put('3.8',0,[grid(['...','.##'],[0,0],[0,2],'从 S 出发，此图向右是到 T 的通道，向下是死路。',current=[0,0]),
        grid(['...','.##'],[0,0],[0,2],'发现右侧 (0,1) 与下方 (1,0)，均记录来自 S。',visited=[[0,0]],frontier=[[0,1],[1,0]],distances={'0,0':0,'0,1':1,'1,0':1},parents={'0,1':'0,0','1,0':'0,0'}),
        grid(['...','.##'],[0,0],[0,2],'处理 (0,1)，发现 T，记录 parent[T]=(0,1)。',visited=[[0,0],[0,1]],frontier=[[1,0],[0,2]],distances={'0,0':0,'0,1':1,'1,0':1,'0,2':2},parents={'0,1':'0,0','1,0':'0,0','0,2':'0,1'}),
        grid(['...','.##'],[0,0],[0,2],'出错：把全部已访问格子当作路径，连下方死路也包含进来。',visited=[[0,0],[0,1],[1,0],[0,2]],warning=True,current=[1,0]),
        grid(['...','.##'],[0,0],[0,2],'正确结果沿前驱回溯，只保留顶行 S→(0,1)→T。',route=[[0,0],[0,1],[0,2]],visited=[[0,0],[0,1],[1,0],[0,2]],distances={'0,0':0,'0,1':1,'1,0':1,'0,2':2},parents={'0,1':'0,0','1,0':'0,0','0,2':'0,1'})])
    levels=[]
    for text,highlight,queue,output,warning in [
        ('本层队列 [B,C]，两个节点各有两个孩子。本层宽度应固定为 2。',[1,2],['B','C'],[],False),
        ('i=0，B 出队，D、E 入队。动态 size 从 2 变为 3。',[1],['C','D','E'],['B'],False),
        ('i=1，C 出队，F、G 入队。动态 size 变为 4。',[2],['D','E','F','G'],['B','C'],False),
        ('出错：i=2 时 2<size(4) 仍成立，D 被错误纳入本层。',[3],['E','F','G'],['B','C','D'],True),
        ('修正：预先固定 width=2，只处理 B、C；下一层保留 D、E、F、G。',[1,2],['D','E','F','G'],['B','C'],False)]:
        f=net(list('ABCDEFG'),[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]],text,highlight,
              {0:['第 0 层'],1:['第 1 层'],2:['第 1 层'],3:['第 2 层'],4:['第 2 层'],5:['第 2 层'],6:['第 2 层']},warning=warning)
        f['containers']=[dict(name='队头 → 队尾',values=queue),dict(name='本层输出',values=output)];levels.append(f)
    put('3.5',0,levels)
    old=cases['3.5'][0];cases['3.5'][0]=(old[0],'本层队列 [B,C]，B 的孩子为 D、E，C 的孩子为 F、G。',*old[2:5],old[5])
    _robot_cases(put)


def _robot_cases(put):
    # Dimensions and physical scales are explicitly carried by the drawing.
    for index in (0,1):
        texts=(['走廊宽 0.8m，机器人直径 1.0m。','把机器人当点，中心线可以通过。','出错：机器人实体越过墙面，发生碰撞。','按半径膨胀障碍后，走廊关闭，拒绝此路。'] if index==0 else
               ['分辨率 0.1m/格，机器人半径 0.3m。','错误将 0.3 直接转为整数，得到 0 格。','出错：没有膨胀障碍，机器人可能碰撞。','ceil(0.3/0.1)=3，按 3 格半径膨胀。'])
        put('6.1',index,[frame(txt,j==2,robot=dict(kind='corridor' if index==0 else 'radius',phase=j)) for j,txt in enumerate(texts)])
    base=['.....','.....','.....'];s=[1,0];t=[1,4]
    put('6.2',0,[grid(base,s,t,'旧地图路径已规划；保留 g/rhs。',route=[[1,c] for c in range(5)],scores={f'1,{c}':dict(g=4-c,rhs=4-c,known=True) for c in range(5)},scoreKind='dstar'),
        grid(['.....','..#..','.....'],s,t,'新增障碍 (1,2)，受影响的旧记录需修复。',current=[1,1],scores={'1,1':dict(g=3,rhs=5,known=True)},scoreKind='dstar'),
        grid(['.....','..#..','.....'],s,t,'出错：清空记录重跑 A* 可以重新找路，但这不是 D* Lite 的状态复用。',warning=True),
        grid(['.....','..#..','.....'],s,t,'D* Lite 保留旧 g，更新 rhs，将不一致节点放入修复队列。',current=[1,1],scores={'1,1':dict(g=3,rhs=5,known=True),'1,3':dict(g=1,rhs=1,known=True)},scoreKind='dstar')])
    put('6.2',1,[grid(base,s,t,'旧起点 (1,0)，last_start=(1,0)，km=0。',route=[[1,0],[1,1]],current=s),
        grid(base,[1,1],t,'起点移动一步到 (1,1)。',current=[1,1]),
        grid(base,[1,1],t,'出错：km 仍为 0，关键字基准没有补偿这一步移动。',current=[1,1],warning=True),
        grid(base,[1,1],t,'h(old,new)=1；更新 km=1、last_start=(1,1)，再修复。',current=[1,1])])
    obstacle=[[4,0,6,4.5],[4,5.5,6,10]]
    def scene(text, points, parents, warning=False, sample=None, route=None, obstacles=None):
        return frame(text,warning,scene=dict(start=[1,5],goal=[9,5],points=points,parents=parents,
              obstacles=obstacles if obstacles is not None else obstacle,sample=sample,route=route or []))
    put('6.3',0,[scene('S 与 P 都在空闲区域，中间有墙。',[[1,5]],[-1],sample=[9,5],obstacles=[[4,2,6,8]]),
        scene('只检查新点 P，端点检测通过。',[[1,5],[9,5]],[-1,-1],obstacles=[[4,2,6,8]]),
        scene('出错：连接 S→P 穿过墙体，线段碰撞。',[[1,5],[9,5]],[-1,0],True,obstacles=[[4,2,6,8]]),
        scene('检查完整线段，拒绝这条边，P 不加入树。',[[1,5]],[-1],sample=[9,5],obstacles=[[4,2,6,8]])])
    points=[[1,5],[2,3],[2,7],[3,2],[3,8]]
    put('6.3',1,[scene('地图中间有窄通道；本次预算为 100 次采样。',[[1,5]],[-1]),
        scene('示意本次树仍在墙左；只显示部分已接受节点，不伪造 100 次完整采样。',points,[-1,0,0,1,2]),
        scene('出错：预算耗尽就宣布无路；图中窄通道实际存在。',points,[-1,0,0,1,2],True),
        scene('应报告预算内未找到，不能据此证明不可达。',points,[-1,0,0,1,2])])
    edges=[[0,1,10],[1,2,2]]
    put('6.4',0,[net(['S','B','C'],edges,'原树 B 代价 10，C 代价 12。',meta={0:['cost 0'],1:['cost 10'],2:['cost 12']}),
        net(['S','B','C'],[[0,1,8],[1,2,2]],'重连 B，经新父路径后代价降为 8；图中 S→B 表示该路径的累计代价。',[1],{1:['cost 8'],2:['cost 12（未更新）']}),
        net(['S','B','C'],[[0,1,8],[1,2,2]],'出错：C 仍记 12，不等于父代价 8 加边代价 2。',[2],{1:['cost 8'],2:['12 ≠ 8+2']},warning=True),
        net(['S','B','C'],[[0,1,8],[1,2,2]],'向后代传播差值 -2，C 更新为 10。',[2],{1:['cost 8'],2:['cost 10']})])
    put('6.4',1,[scene('运行 500 次采样，以下只显示当前路径的节点。',[[1,5],[5,2],[9,5]],[-1,0,1],obstacles=[],route=[[1,5],[5,2],[9,5]]),
        scene('出错：有限样本得到一条路径，不能据此宣称全局最优。',[[1,5],[5,2],[9,5]],[-1,0,1],True,obstacles=[],route=[[1,5],[5,2],[9,5]]),
        scene('此无障碍示意中还存在直线路径；有限搜索只报告当前找到的最好路径。',[[1,5],[5,2],[9,5]],[-1,0,1],obstacles=[],route=[[1,5],[9,5]])])
    for index in (0,1):
        points=([[t/10,1-(t/10-.5)**2] for t in range(11)] if index else [[t,2*t] for t in range(6)])
        texts=(['s(τ)=10τ，τ=t/5；把时间换成秒。','t=2.5s 时 s=5m，ds/dτ=10。','出错：把 ds/dτ=10 当作 10m/s，漏除以 T=5。','ds/dt=10/5=2m/s，与位置曲线斜率一致。'] if not index else
               ['速度曲线 v(t)=1-(t-0.5)²，限制 0.9。','只检查 t=0、1，端点均为 0.75。','出错：端点合格就接受，遗漏中间超限的速度。','检查导数为零的位置 t=0.5，v=1>0.9，拒绝轨迹。'])
        put('6.5',index,[frame(txt,j==2,plot=dict(points=points,xLabel='t / s',yLabel='v / (m/s)' if index else 's / m',
                     limit=.9 if index else None,marked=([0,10] if j<3 else [0,5,10]) if index else [min(j,5)])) for j,txt in enumerate(texts)])
