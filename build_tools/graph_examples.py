"""Shared ten-node graph and execution traces for the search lessons."""
from collections import deque

TREE=[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(3,7),(4,8),(6,9)]
EDGES=TREE+[(4,5),(8,9)]
POSITIONS=[(210,28),(105,88),(315,88),(40,155),(145,155),(255,155),(380,155),(40,220),(145,220),(325,220)]

def graph_for(id):
    edges=TREE if id=='3.5' else EDGES
    directed=id=='3.3'
    g=[[] for _ in range(10)]
    for a,b in edges:
        g[a].append(b)
        if not directed and id!='3.5':g[b].append(a)
    return g,edges,directed

def trace(id):
    if id in ('2.1','2.2'):return recursion_trace(id)
    if id in ('3.7','3.8'):return grid_trace(id)
    if id not in ('3.1','3.2','3.3','3.4','3.5','3.6'):return None
    g,edges,directed=graph_for(id)
    numeric=id=='3.5'
    label=lambda n:str(n+1) if numeric else chr(65+n)
    diagram={'nodes':[[label(n),x,y] for n,(x,y) in enumerate(POSITIONS)],'edges':edges,'directed':directed}
    frames=[]
    def add(text,active=(),cells=()):
        frames.append({'cells':list(cells),'text':text,'active':[],'diagram':diagram,'highlight':list(active)})
    show=lambda values:' → '.join(label(n) for n in values) or '空'
    add('10 个节点。'+('树按层次排列。' if numeric else '起点 A；邻居按图中编号顺序处理。'))
    if id=='3.1':
        seen=set();path=[]
        def dfs(u):
            seen.add(u);path.append(u);add('进入 '+label(u)+'，标记已访问。',[u],['调用栈：'+show(path)])
            for v in g[u]:
                if v not in seen:dfs(v)
            path.pop();add('从 '+label(u)+' 返回上一层。',path[-1:],['调用栈：'+show(path)])
        dfs(0)
    elif id=='3.2':
        stack=[0];seen={0};order=[]
        while stack:
            u=stack.pop();order.append(u)
            for v in reversed(g[u]):
                if v not in seen:seen.add(v);stack.append(v)
            add('弹出并处理 '+label(u)+'；右端为栈顶。',[u],['栈：'+show(stack),'已处理：'+show(order)])
    elif id=='3.3':
        path=[];on=set();count=0
        def dfs(u):
            nonlocal count
            path.append(u);on.add(u);add('选择 '+label(u),path,['当前路径：'+show(path)])
            if u==9:
                count+=1;add('找到第 '+str(count)+' 条 A 到 J 的路径。',path,['结果：'+show(path)])
            else:
                for v in g[u]:
                    if v not in on:dfs(v)
            path.pop();on.remove(u);add('撤销 '+label(u)+'，继续其他分支。',path,['当前路径：'+show(path)])
        dfs(0)
    elif id=='3.5':
        q=deque([0]);depth=0
        while q:
            layer=[q.popleft() for _ in range(len(q))]
            for u in layer:q.extend(g[u])
            add('第 '+str(depth)+' 层；先固定本层长度再处理。',layer,['当前层：'+show(layer),'下一层队列：'+show(q)])
            depth+=1
    else:
        q=deque([0]);dist=[-1]*10;parent=[-1]*10;dist[0]=0;order=[]
        while q:
            u=q.popleft();order.append(u);new=[]
            for v in g[u]:
                if dist[v]==-1:
                    dist[v]=dist[u]+1;parent[v]=u;q.append(v);new.append(v)
            add('处理 '+label(u)+'，距离 '+str(dist[u])+'；新发现：'+show(new),[u]+new,['队列：'+show(q),'已处理：'+show(order)])
        if id=='3.6':
            path=[];u=9
            while u!=-1:path.append(u);u=parent[u]
            path.reverse();add('A 到 J 的最短路径共 '+str(dist[9])+' 条边。',path,['最短路径：'+show(path)])
    return frames

def recursion_trace(id):
    n=3 if id=='2.1' else 2
    frames=[];stack=[];logs=[]
    def add(text,equation='',returned=''):
        frames.append({'cells':[],'active':[],'text':text,'recursion':{
            'stack':list(stack),'equation':equation,'returned':returned,
            'logs':list(logs) if id=='2.2' else None}})
    add(f'main 准备调用 sum({n})。','等待函数调用')
    for value in range(n,-1,-1):
        stack.append(value)
        if id=='2.2':logs.append(f'进入 {value}')
        add(f'sum({value}) 入栈。'+('命中基例，返回 0。' if value==0 else '当前调用等待下一层返回。'),
            'sum(0) = 0' if value==0 else f'sum({value}) = {value} + sum({value-1})')
    stack.pop();result=0
    add('sum(0) 出栈，把 0 交给 sum(1)。','返回到上一层','sum(0) → 0')
    for value in range(1,n+1):
        smaller=result;result=value+smaller
        if id=='2.2':logs.append(f'返回 {value}')
        add(f'恢复 sum({value})，读取下一层返回的 {smaller}，计算得到 {result}。',
            f'sum({value}) = {value} + {smaller} = {result}')
        stack.pop()
        add(f'sum({value}) 出栈，'+('main 收到最终结果。' if not stack else '把结果交给上一层。'),
            f'最终结果：{result}' if not stack else '上一层恢复执行',f'sum({value}) → {result}')
    if id=='2.2':
        logs.append(f'结果: {result}');add('main 打印最终结果。注意基例直接 return，不会打印“返回 0”。',f'最终结果：{result}')
    return frames

def grid_trace(id):
    grid=['....','.##.','....']; rows,cols=3,4
    frames=[];seen=set();path=[];distance={};pending=deque();parent={}
    def add(text,current=None,route=()):
        frames.append({'cells':[],'active':[],'text':text,'grid':grid,
                       'visited':[list(x) for x in seen],'current':current,
                       'route':[list(x) for x in route],
                       'frontier':[list(x) for x in pending],
                       'distances':{f'{r},{c}':d for (r,c),d in distance.items()}})
    add('起点 S=(0,0)，终点 T=(2,3)。仅上下左右移动，深色格子为障碍。')
    def neighbors(r,c):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]!='#':yield nr,nc
    if id=='3.7':
        def dfs(r,c):
            seen.add((r,c));path.append((r,c));add(f'进入 ({r},{c})，标记已访问。',[r,c],path)
            if (r,c)==(2,3):
                add(f'DFS 找到一条路径，共 {len(path)-1} 步；不保证最短。',[r,c],path);return True
            for nr,nc in neighbors(r,c):
                if (nr,nc) not in seen and dfs(nr,nc):return True
            path.pop();add(f'({r},{c}) 无新方向，返回上一格。',list(path[-1]) if path else None,path)
            return False
        dfs(0,0)
    else:
        pending.append((0,0));seen.add((0,0));distance[(0,0)]=0
        while pending:
            r,c=pending.popleft()
            for v in neighbors(r,c):
                if v not in seen:
                    seen.add(v);distance[v]=distance[(r,c)]+1;parent[v]=(r,c);pending.append(v)
            add(f'出队 ({r},{c})，距离 {distance[(r,c)]}；橙色格子仍在队列中。',[r,c])
        cur=(2,3);route=[cur]
        while cur!=(0,0):cur=parent[cur];route.append(cur)
        add(f'BFS 最短路径为 {distance[(2,3)]} 步；绿色展示一条最短路线。',[2,3],route[::-1])
    return frames
