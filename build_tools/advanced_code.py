"""Extract executable Python definitions, never copy unrelated lesson code."""
import ast
from pathlib import Path
from advanced_cpp import code as cpp_code

DEPS={
 '4.1':['subsets'],'4.2':['select_intervals'],'4.3':['merge_sort'],
 '4.4':['climb_stairs'],'4.5':['knapsack'],'4.6':['lcs'],
 '5.1':['components'],'5.2':['dijkstra'],'5.3':['grid_astar'],
 '5.4':['floyd_warshall'],'5.5':['topological_sort'],'5.6':['DSU'],
 '5.7':['DSU','kruskal'],'6.1':['grid_astar'],'6.2':['DStarLite'],
 '6.3':['collision_free','rrt'],'6.4':['collision_free','rrt'],'6.5':['quintic_trajectory']}
MAIN={
'4.1': 'for row in subsets([1, 2, 3, 4]):\n    print(row)',
'4.2': 'print(select_intervals([(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,9)]))',
'4.3': 'print(merge_sort([8, 3, 7, 1, 9, 2, 6, 4, 5]))',
'4.4': 'for n in [0, 1, 5, 9]:\n    print(n, climb_stairs(n))',
'4.5': 'print(knapsack([2,3,4,5], [3,4,5,8], 9))\nprint(knapsack([2], [3], 4))',
'4.6': 'print(lcs("ABCBDAB", "BDCABA"))',
'5.1': '''graph = [[] for _ in range(10)]
for u, v in [(0,1),(1,2),(2,3),(4,5),(5,6),(7,8)]:
    graph[u].append(v)
    graph[v].append(u)
print(components(graph))''',
'5.2': '''graph = [[] for _ in range(10)]
for u, v, w in [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,4,5),(3,5,3),
                 (4,5,1),(5,6,2),(6,7,1),(7,8,2),(8,9,1)]:
    graph[u].append((v,w))
distance, parent = dijkstra(graph, 0)
print("distance:", distance)
route, u = [], 9
if math.isfinite(distance[u]):
    while u != -1:
        route.append(u)
        u = parent[u]
print("route:", route[::-1])''',
'5.3': '''grid = ['.........','.###.###.','...#.....','...#.###.','.........','..###....']
route = grid_astar(grid, (0,0), (5,8))
print("steps:", len(route)-1 if route else "unreachable")
print(route)''',
'5.4': '''inf = math.inf
matrix = [[0,3,10,inf],[inf,0,4,8],[inf,inf,0,2],[1,inf,inf,0]]
for row in floyd_warshall(matrix):
    print(row)''',
'5.5': '''graph = [[2,3],[3],[4],[4,5],[6],[7],[8],[8],[9],[]]
print(topological_sort(graph))
try:
    topological_sort([[1],[0]])
except ValueError as error:
    print(error)''',
'5.6': '''dsu = DSU(10)
for a,b in [(0,1),(2,3),(1,2),(4,5),(6,7),(5,6),(8,9),(3,7),(0,9),(1,9)]:
    print(a,b, "merged:", dsu.union(a,b), "components:", dsu.count)
print("representatives:", [dsu.find(i) for i in range(10)])''',
'5.7': '''total, edges, count = kruskal(5, [(1,0,1),(4,0,2),(2,1,2),(3,1,3),(5,2,4),(1,3,4)])
print("MST" if count == 1 else "minimum spanning forest", total, edges)''',
'6.1': '''grid = ['.........','.###.###.','...#.....','...#.###.','.........','..###....']
for heuristic in [False, True]:
    route = grid_astar(grid, (0,0), (5,8), heuristic=heuristic)
    print("A*" if heuristic else "uniform cost", "steps:", len(route)-1 if route else "unreachable")
    print(route)''',
'6.2': '''grid = ['.........','.###.###.','...#.....','...#.###.','.........','..###....']
planner = DStarLite(grid, (0,0), (5,8))
planner.repair()
before = planner.path()
print("initial:", before)
changed = before[len(before)//2]
planner.change(changed, True)
planner.repair()
print("repaired:", planner.path())
planner.change(changed, False)
planner.move(before[1])
planner.repair()
print("restored and moved:", planner.path())''',
'6.3': '''points, parents, costs, route = rrt((1,1), (9,9), [(3,2,6,7)], 250, 7, False)
print("nodes:", len(points))
print("route:", route or "not found within budget")
print("length:", sum(math.dist(a,b) for a,b in zip(route,route[1:])))''',
'6.4': '''points, parents, costs, route = rrt((1,1), (9,9), [(3,2,6,7)], 250, 7, True)
print("nodes:", len(points))
print("route:", route or "not found within budget")
print("length:", sum(math.dist(a,b) for a,b in zip(route,route[1:])))''',
'6.5': '''distance, max_velocity, max_acceleration = 10, 2, 1
duration = max(15/8*abs(distance)/max_velocity,
               math.sqrt(10*math.sqrt(3)/3*abs(distance)/max_acceleration))
print("T:", duration)
print("t,s,v,a")
for row in quintic_trajectory(distance, duration):
    print(",".join(f"{value:.6f}" for value in row))'''}

def code_for(id):
    source=Path(__file__).with_name('advanced_algorithms.py').read_text(encoding='utf-8')
    definitions={node.name:ast.get_source_segment(source,node) for node in ast.parse(source).body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
    selected=['emit_state']+DEPS[id]
    python='"""Standalone Python 3 example. Edit main() to try another case."""\nimport math\nimport heapq\nimport random\nfrom collections import deque\n\n\n'
    python+='\n\n\n'.join(definitions[name] for name in selected)
    python+='\n\n\ndef main():\n'+'\n'.join('    '+line for line in MAIN[id].splitlines())
    python+='\n\n\nif __name__ == "__main__":\n    main()\n'
    return cpp_code(id),python
