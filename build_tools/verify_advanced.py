"""Deterministic algorithm/property checks and standalone program smoke tests."""
from pathlib import Path
import ast
import itertools
import math
import random
import subprocess
import tempfile
import os
import re
import json
import advanced_algorithms as a
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
from advanced_lessons import RECORDS
from advanced_demos import presets

ROOT=Path(__file__).resolve().parent.parent
RNG=random.Random(42)

def pages():
    class Links(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links=[]
        def handle_starttag(self,tag,attrs):
            self.links.extend(value for name,value in attrs if name in ('href','src') and value)
    files=[ROOT/'index.html']+list((ROOT/'lessons').rglob('*.html'))+list((ROOT/'codes').rglob('*.html'))
    for file in files:
        source=file.read_text(encoding='utf-8')
        assert '\ufffd' not in source
        parser=Links();parser.feed(source)
        for link in parser.links:
            parsed=urlparse(link)
            if parsed.scheme or link.startswith('#'):continue
            target=file.parent/unquote(parsed.path)
            assert target.exists(),(file,link)
        if file.parent.name in ('stage-4','stage-5','stage-6') and file.parent.parent.name=='lessons':
            payload=re.search(r'<script id="lesson-presets" type="application/json">(.*?)</script>',source,re.S)
            assert payload,file
            assert len(json.loads(payload.group(1)))==3
    print(f'{len(files)} HTML pages: local links, downloads and embedded JSON passed.',flush=True)

def checks():
    for n in range(8):
        output=a.subsets(list(range(n)))
        assert len(output)==len(set(map(tuple,output)))==2**n
    for _ in range(50):
        nums=[RNG.randint(-5,5) for _ in range(RNG.randrange(15))]
        assert a.merge_sort(nums)==sorted(nums)
        intervals=[(RNG.randrange(8),RNG.randrange(8,15)) for _ in range(6)]
        best=max(len(group) for k in range(7) for group in itertools.combinations(intervals,k)
                 if all(x[1]<=y[0] or y[1]<=x[0] for x,y in itertools.combinations(group,2)))
        assert len(a.select_intervals(intervals))==best
        weights=[RNG.randrange(1,6) for _ in range(6)]
        values=[RNG.randrange(-2,12) for _ in weights]
        capacity=RNG.randrange(10)
        expected=max(sum(values[i] for i in range(6) if mask>>i&1) for mask in range(64)
                     if sum(weights[i] for i in range(6) if mask>>i&1)<=capacity)
        assert a.knapsack(weights,values,capacity)==expected
    assert [a.climb_stairs(i) for i in range(6)]==[1,1,2,3,5,8]
    for first,second,length in [('ABCBDAB','BDCABA',4),('','abc',0),('aaaa','aa',2),('abc','xyz',0)]:
        size,seq=a.lcs(first,second)
        assert size==len(seq)==length
        for source in (first,second):
            it=iter(source)
            assert all(any(c==wanted for c in it) for wanted in seq)
    for _ in range(30):
        n=8;matrix=[[0 if i==j else math.inf for j in range(n)] for i in range(n)]
        graph=[[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i!=j and RNG.random()<0.2:
                    weight=RNG.randrange(8);graph[i].append((j,weight));matrix[i][j]=weight
        expected=a.floyd_warshall(matrix)
        for start in range(n):assert a.dijkstra(graph,start)[0]==expected[start]
    for _ in range(20):
        rows,cols=6,9
        grid=[['#' if RNG.random()<0.2 else '.' for _ in range(cols)] for _ in range(rows)]
        grid[0][0]=grid[-1][-1]='.'
        start,goal=(0,0),(rows-1,cols-1)
        planner=a.DStarLite(grid,start,goal)
        for change in range(12):
            planner.repair()
            expected=a.grid_astar(grid,start,goal,heuristic=False)
            result=planner.path()
            assert len(result)==len(expected),(result,expected)
            assert len(a.grid_astar(grid,start,goal))==len(expected)
            if result and len(result)>1 and change%3==0:
                start=result[1];planner.move(start)
            else:
                cell=(RNG.randrange(rows),RNG.randrange(cols))
                if cell in (start,goal):continue
                blocked=grid[cell[0]][cell[1]]!='#'
                grid[cell[0]][cell[1]]='#' if blocked else '.'
                planner.change(cell,blocked)
    for star in (False,True):
        obstacles=[(3,2,6,7)]
        for seed in range(5):
            points,parent,cost,route=a.rrt((1,1),(9,9),obstacles,250,seed,star)
            for j in range(1,len(points)):
                assert a.collision_free(points[j],points[parent[j]],obstacles)
                assert math.isclose(cost[j],cost[parent[j]]+math.dist(points[j],points[parent[j]]),abs_tol=1e-8)
                seen=set();u=j
                while u!=-1:assert u not in seen;seen.add(u);u=parent[u]
            for u,v in zip(route,route[1:]):assert a.collision_free(u,v,obstacles)
    assert not a.collision_free((0,0),(10,10),[(3,3,4,4)])
    assert not a.collision_free((0,3),(10,3),[(3,3,4,4)])
    assert a.collision_free((0,0),(0,10),[(3,3,4,4)])
    for duration in (1,5,10):
        samples=a.quintic_trajectory(10,duration,100)
        assert samples[0]==(0,0,0,0)
        assert all(abs(x-y)<1e-8 for x,y in zip(samples[-1],(duration,10,0,0)))
        assert max(row[2] for row in samples)<=15/8*10/duration+1e-8
    assert a.kruskal(3,[(1,0,1),(2,1,2),(5,0,2)])[0]==3
    assert a.kruskal(4,[(1,0,1)])[2]==3
    for bad in ([[1],[0]],[[0]]):
        try:a.topological_sort(bad)
        except ValueError:pass
        else:raise AssertionError('cycle not detected')
    for record in RECORDS:
        cases=presets(record[0])
        assert len(cases)==3
        for case in cases:
            assert case['frames']
            json.dumps(case,allow_nan=False)
    print('Algorithm properties and all 54 scenario traces passed.',flush=True)

def programs():
    compiler=Path('E:/Programs/MinGW-w64/ucrt64/bin/g++.exe')
    env=os.environ.copy();env['PATH']=str(compiler.parent)+os.pathsep+env.get('PATH','')
    files=[p for stage in (4,5,6) for p in (ROOT/'codes'/f'stage-{stage}').glob('*.cpp')]
    assert len(files)==18
    with tempfile.TemporaryDirectory(prefix='algorithm-check-',dir='D:/Users/mio/Desktop/Study',ignore_cleanup_errors=True) as tmp:
        for source in files:
            target=Path(tmp)/(source.name[:3]+'.exe')
            subprocess.run([str(compiler),'-std=c++17','-Wall','-Wextra','-O1',str(source),'-o',str(target)],
                           check=True,capture_output=True,timeout=60,env=env)
            result=subprocess.run([str(target)],check=True,capture_output=True,timeout=15,env=env)
            assert result.stdout
            output=result.stdout.decode('utf-8').replace('\r\n','\n')
            id=source.name[:3].replace('-','.')
            expected={'4.2':'count=3','4.3':'1 2 3 4 5 6 7 8 9','4.4':'9: 55',
                      '4.5':'13\n3','5.1':'components=4','5.2':'J: 13','5.3':'steps=13',
                      '5.5':'dependency cycle','5.6':'components=1','5.7':'total=7',
                      '6.1':'same optimal length=1','6.2':'restored steps=13','6.5':'T=9.375000'}
            if id in expected: assert expected[id] in output,(id,output)
            if id=='4.1':assert len(output.strip().splitlines())==16
            if id=='4.6':assert output.startswith('4 ')
            if id=='5.4':assert output.splitlines()[0].split()==['0','3','7','9']
            if id in ('6.3','6.4'):
                assert 'length=' in output
                coords=[tuple(map(float,row.split(','))) for row in output.splitlines()[2:]]
                assert coords[0]==(1,1) and coords[-1]==(9,9)
                for p,q in zip(coords,coords[1:]):assert a.collision_free(p,q,[(3,2,6,7)])
            python=source.with_suffix('.py')
            ast.parse(python.read_text(encoding='utf-8'))
            result=subprocess.run([os.sys.executable,str(python)],check=True,capture_output=True,timeout=15,env=env)
            assert result.stdout
            print('C++ / Python passed:',source.name[:3],flush=True)

if __name__=='__main__':
    pages()
    checks()
    programs()
