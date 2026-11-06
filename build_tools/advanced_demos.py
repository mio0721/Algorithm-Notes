"""Build reproducible traces by executing the same Python algorithms as downloads."""
import copy
import math
import advanced_algorithms as a

GRID = ['.........','.###.###.','...#.....','...#.###.','.........','..###....']
EDGES = [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,4,5),(3,5,3),
         (4,5,1),(5,6,2),(6,7,1),(7,8,2),(8,9,1)]

def graph(n, edges, directed=False, layout=None):
    if layout == 'forest':
        # A union-find parent forest may change edges at each step; fixed
        # circular positions prevent a new parent edge passing through a node.
        positions=[(225+170*math.cos(-math.pi/2+2*math.pi*i/n),
                    165+125*math.sin(-math.pi/2+2*math.pi*i/n)) for i in range(n)]
    elif layout == 'dag':
        positions=[(65,45),(275,45),(65,120),(195,120),(120,195),
                   (315,195),(95,270),(290,320),(385,270),(435,320)]
    elif n == 10:
        # The default weighted network has triangles and a tail. Arrange its
        # actual endpoints so no edge crosses another edge or unrelated node.
        positions=[(40,160),(130,95),(130,225),(235,55),(235,265),
                   (290,160),(370,210),(370,65),(435,100),(435,180)]
    elif n == 5:
        positions=[(75,110),(185,45),(185,175),(340,70),(340,225)]
    elif n == 4:
        positions=[(80,55),(320,55),(320,270),(80,270)]
    else:
        positions=[(55+(i%4)*115,45+(i//4)*110) for i in range(n)]
    nodes=[[chr(65+i),x,y] for i,(x,y) in enumerate(positions)]
    return dict(nodes=nodes,
                edges=edges, directed=directed, viewBox=[0,0,470,350])

def run(id, variant):
    frames = []
    def emit(frame):
        frames.append(copy.deepcopy(frame))
    def note(text, **kwargs):
        a.emit_state(emit,text,**kwargs)
    if id == '4.1':
        nums = ([1,2,3,4], [], [2,5,8])[variant]
        result = a.subsets(nums,emit)
        paths=[tuple(row) for row in result]
        nodes=[];edges=[];positions={};leaf=[0]
        def place(path):
            children=[p for p in paths if len(p)==len(path)+1 and p[:-1]==path]
            locations=[place(child) for child in children]
            if locations: x=sum(locations)/len(locations)
            else: x=leaf[0];leaf[0]+=1
            positions[path]=x
            return x
        place(())
        for index,path in enumerate(paths):
            x=25+positions[path]/max(1,leaf[0]-1)*400
            nodes.append(['∅' if not path else str(path[-1]),x,30+len(path)*70])
            if path:edges.append((paths.index(path[:-1]),index))
        for f in frames:
            path=tuple(int(x) for x in f['cells'])
            f['network']=dict(nodes=nodes,edges=edges,directed=True)
            f['highlight']=[paths.index(path)]
        note(f'共 {len(result)} 个子集；空集也计入。', matrix=[list(map(str,row))+['']*(len(nums)-len(row)) for row in result],
             rowLabels=list(range(len(result))),colLabels=list(range(len(nums))))
    elif id == '4.2':
        data = ([(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,9)],
                [(0,3),(3,6),(2,4)],[(1,8),(2,7),(3,6),(4,5)])[variant]
        ordered=sorted(data,key=lambda p:(p[1],p[0]))
        chosen=a.select_intervals(data,emit)
        for i,f in enumerate(frames):
            f['intervals']=dict(all=ordered,current=i,chosen=chosen[:0])
            f['intervals']['chosen']=[list(p) for p in chosen if p in ordered[:i+1]]
        note(f'最多保留 {len(chosen)} 个区间。',intervals=dict(all=ordered,current=-1,chosen=chosen))
    elif id == '4.3':
        data=([8,3,7,1,9,2,6,4,5],[9,8,7,6,5,4,3,2,1],[3,1,3,2,2,1,3,1,2])[variant]
        result=a.merge_sort(data,emit)
        note('排序完成。',cells=result,indexed=True)
    elif id == '4.4':
        n=(9,0,1)[variant]
        result=a.climb_stairs(n,emit)
        note(f'n={n}，方案数 {result}。',cells=frames[-1]['cells'],indexed=True)
    elif id == '4.5':
        weights,values,capacity=(([2,3,4,5],[3,4,5,8],9),([2],[3],4),([5,6],[8,9],3))[variant]
        result=a.knapsack(weights,values,capacity,emit)
        for f in frames: f['text']='物品 (重量,价值)：'+str(list(zip(weights,values)))+'；'+f['text']
        note(f'最大价值 {result}。',cells=frames[-1]['cells'],indexed=True)
    elif id == '4.6':
        first,second=(('ABCBDAB','BDCABA'),('abc','xyz'),('','abc'))[variant]
        length,sequence=a.lcs(first,second,emit)
        visual={k:v for k,v in frames[-1].items() if k in ('matrix','rowLabels','colLabels')} if frames else {}
        note(f'输入 {first!r} 与 {second!r}；长度 {length}，一个LCS为 {sequence!r}。',**visual)
    elif id == '5.1':
        edges=([(0,1),(1,2),(2,3),(4,5),(5,6),(7,8)],[(i,i+1) for i in range(9)],[])[variant]
        adjacency=[[] for _ in range(10)]
        for u,v in edges: adjacency[u].append(v);adjacency[v].append(u)
        result=a.components(adjacency,emit)
        note(f'共 {len(result)} 个连通分量：{result}。')
        for f in frames:f['network']=graph(10,edges)
    elif id == '5.2':
        edges=(EDGES,EDGES[:-2],[(0,1,-1)])[variant]
        adjacency=[[] for _ in range(10)]
        for u,v,w in edges:adjacency[u].append((v,w))
        try:
            distance,parent=a.dijkstra(adjacency,0,emit)
            route=[];u=9
            if math.isfinite(distance[u]):
                while u!=-1:route.append(u);u=parent[u]
                route.reverse()
            note('终点J：'+('不可达' if not route else f'最短代价 {distance[9]}'),route=route,
                 distances=distance, parents=parent,
                 settled=[i for i,d in enumerate(distance) if math.isfinite(d)])
        except ValueError as error:note(str(error))
        for f in frames:f['network']=graph(10,edges,True)
    elif id in ('5.3','6.1'):
        data=(GRID,['.........']*6,['....#....']*6)[variant]
        a.grid_astar(data,(0,0),(5,8),emit)
    elif id == '5.4':
        inf=math.inf
        matrix=([[0,3,10,inf],[inf,0,4,8],[inf,inf,0,2],[1,inf,inf,0]],
                [[0,-2,9],[inf,0,3],[inf,inf,0]],[[0,1,inf],[inf,0,-3],[1,inf,0]])[variant]
        note('初始化：自身0，无边∞；k必须是最外层。',matrix=matrix)
        try:
            result=a.floyd_warshall(matrix,emit)
            note('所有点对距离计算完毕；对角线上没有负数。',matrix=result)
        except ValueError as error: note(str(error),matrix=frames[-1]['matrix'])
    elif id == '5.5':
        adjacency=([[2,3],[3],[4],[4,5],[6],[7],[8],[8],[9],[]],
                   [[1],[2],[0],[],[],[],[],[],[],[]],[[] for _ in range(10)])[variant]
        try:note('拓扑顺序：'+str(a.topological_sort(adjacency,emit)))
        except ValueError as error:note(str(error))
        for f in frames:f['network']=graph(10,[(u,v) for u,row in enumerate(adjacency) for v in row],True,layout='dag')
    elif id == '5.6':
        operations=([(0,1),(2,3),(1,2),(4,5),(6,7),(5,6),(8,9),(3,7),(0,9),(1,9)],
                    [(0,1),(0,1),(1,0)],[(i,i+1) for i in range(9)])[variant]
        dsu=a.DSU(10)
        note('10个独立集合，parent[i]=i。',cells=dsu.parent,indexed=True)
        for u,v in operations:
            merged=dsu.union(u,v)
            roots=[dsu.find(i) for i in range(10)]
            note(f'union({u},{v})：'+('合并成功' if merged else '已经连通，不重复合并')+f'；分量 {dsu.count}。',
                 cells=dsu.parent,indexed=True,network=graph(10,[(i,dsu.parent[i]) for i in range(10) if i!=dsu.parent[i]],True,layout='forest'),
                 highlight=[u,v],matrix=[list(range(10)),roots],rowLabels=['顶点','代表'])
    elif id == '5.7':
        edges=([(w,u,v) for u,v,w in EDGES]+[(6,1,4),(9,3,7)],
               [(1,0,1),(2,1,2),(5,0,2),(1,3,4)],
               [(-2,0,1),(1,1,2),(1,2,3),(1,0,3)])[variant]
        n=(10,5,4)[variant]
        total,chosen,count=a.kruskal(n,edges,emit)
        note(f'总权 {total}；'+('得到最小生成树' if count==1 else f'非连通：得到 {count} 棵树的森林'),chosenEdges=chosen)
        for f in frames:f['network']=graph(n,[(u,v,w) for w,u,v in edges])
    elif id == '6.2':
        data=GRID if variant<2 else ['.........']*6
        planner=a.DStarLite(data,(0,0),(5,8))
        planner.repair(emit)
        route=planner.path()
        note(f'首次规划完成：{len(route)-1} 步。',grid=data,start=planner.start,goal=planner.goal,route=route,scores=planner.scores(),scoreKind='dstar')
        if variant == 2:
            changed=[(r,4) for r in range(6)]
        else:changed=[route[len(route)//2]]
        for cell in changed:planner.change(cell,True)
        note('发现障碍：复用原g/rhs，开始修复。',grid=[''.join(r) for r in planner.grid],start=planner.start,goal=planner.goal,scores=planner.scores(),scoreKind='dstar')
        planner.repair(emit)
        route=planner.path()
        note('修复结果：'+(f'{len(route)-1} 步' if route else '不可达'),grid=[''.join(r) for r in planner.grid],start=planner.start,goal=planner.goal,route=route,scores=planner.scores(),scoreKind='dstar')
        if variant==1:
            for cell in changed:planner.change(cell,False)
            if route:planner.move(route[1])
            planner.repair(emit)
            note('移除障碍并移动起点后再次修复；km='+str(planner.km),grid=[''.join(r) for r in planner.grid],start=planner.start,goal=planner.goal,route=planner.path(),scores=planner.scores(),scoreKind='dstar')
    elif id in ('6.3','6.4'):
        obstacles=([(3,2,6,7)],[],[(4.5,0,5.5,10)])[variant]
        points,parents,costs,route=a.rrt((1,1),(9,9),obstacles,180,7+variant,id=='6.4',emit)
        # Keep one frame per accepted extension. Snapshots include the entire rewired tree.
        if frames:
            last=copy.deepcopy(frames[-1])
            last['text']='预算结束：'+(f'找到可行路径，长度 {sum(math.dist(p,q) for p,q in zip(route,route[1:])):.3f}。' if route else '未找到；有限采样不能证明无路。')
            frames.append(last)
    elif id=='6.5':
        distance,duration=((10,10),(10,5),(0,10))[variant]
        samples=a.quintic_trajectory(distance,duration,40,emit)
        for frame in frames:frame['chart']=dict(all=samples,current=len(frame.pop('samples'))-1)
        note(f'解析峰值：v={15/8*abs(distance)/duration:.3f}；|a|={10*math.sqrt(3)/3*abs(distance)/duration**2:.3f}。',chart=dict(all=samples,current=40))
    return frames or [dict(text='空输入，无需迭代。',cells=[],active=[])]

NAMES={
 '4.1':['四元素完整搜索树','空集边界','三元素子集'],
 '4.2':['九个任务','最短区间反例','全部重叠'],
 '4.3':['九元素乱序','完全逆序','大量重复值'],
 '4.4':['九级台阶','零级边界','一级边界'],
 '4.5':['容量9的0/1背包','检查重复使用错误','物品全部放不下'],
 '4.6':['多个最优子序列','没有公共字符','空字符串'],
 '5.1':['四个连通分量','全部连通','十个孤立点'],
 '5.2':['十节点带权图','终点不可达','拒绝负权'],
 '5.3':['障碍地图','开放地图','墙体隔断'],
 '5.4':['正权全点对','负边但无负环','检测负环'],
 '5.5':['十任务依赖','存在依赖环','没有依赖'],
 '5.6':['十节点合并','重复合并','链式连接'],
 '5.7':['十节点网络','不连通森林','负权与同权'],
 '6.1':['障碍地图','开放地图','不可达地图'],
 '6.2':['出现新障碍','移除障碍及起点移动','新增墙体导致无路'],
 '6.3':['绕过矩形障碍','无障碍','隔断地图'],
 '6.4':['重连与成本传播','开放空间优化','预算内失败'],
 '6.5':['10米/10秒','时间减半','静止轨迹']}

def clean(value):
    if isinstance(value,float) and not math.isfinite(value):return '∞' if value>0 else '−∞'
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    return value

def presets(id):
    return [dict(name=name,frames=clean(run(id,i))) for i,name in enumerate(NAMES[id])]
