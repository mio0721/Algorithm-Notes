"""Generate focused includes and Chinese annotated standalone programs."""
import ast
import re
from html import escape
from course_flow import FLOW

HEADERS={
'iostream':(r'\b(cout|cin|cerr|endl)\b','控制台输入与输出'),
'vector':(r'\bvector\b','动态数组、邻接表或状态表'),
'string':(r'\b(string|to_string|getline)\b','字符串存储与操作'),
'queue':(r'\b(queue|priority_queue)\s*<','先进先出队列或优先队列'),
'deque':(r'\bdeque\b','双端队列'),
'stack':(r'\bstack\s*<','后进先出的显式栈'),
'unordered_map':(r'\bunordered_map\b','哈希映射，按键查找记录'),
'unordered_set':(r'\bunordered_set\b','哈希集合，判断元素是否出现'),
'map':(r'\bmap\b','有序映射，按节点保存状态'),
'set':(r'\bset\b','有序集合或路径内去重'),
'functional':(r'\b(function|greater|less)\b','递归函数包装或堆比较器'),
'algorithm':(r'(?<![\w.])(?:std::)?(sort|stable_sort|reverse|min|max|copy|fill|lower_bound|upper_bound)\s*\(','排序、取最值、合并或反转等标准算法'),
'utility':(r'\b(pair|make_pair|swap|move)\b','二元组、交换或移动对象'),
'tuple':(r'\b(tuple|tie|make_tuple|get)\b','多字段状态与字典序比较'),
'limits':(r'\bnumeric_limits\b','整数边界或浮点无穷大'),
'numeric':(r'\b(iota|accumulate)\b','连续编号初始化或累加'),
'cmath':(r'\b(sqrt|pow|hypot|abs|isfinite|log|ceil|floor)\s*\(','距离、幂、平方根或数值判断'),
'random':(r'\b(mt19937|uniform_real_distribution|uniform_int_distribution)\b','可复现实验的随机采样'),
'iomanip':(r'\b(setprecision|fixed|setw)\b','控制输出精度与格式'),
'stdexcept':(r'\b(invalid_argument|runtime_error|out_of_range)\b','明确报告非法输入'),
'array':(r'\barray\b','固定长度坐标或障碍边界'),
'cstddef':(r'\bsize_t\b','标准无符号大小类型'),
}

NOTES={
'0.1':[(r'while|for','这一轮核心操作执行多少次，取决于循环变量怎样变化；观察次数而不只看运行秒数。')],
'0.2':[(r'push_back|append','把新读数追加到末尾；容量不足时可能搬迁底层存储。'),(r'\bvector|nums\s*=','保存一串按位置编号的数据，编号从0开始。')],
'0.3':[(r'\bfind\b|\.get\(| in ','只查询已有键，不为了检查存在而插入默认记录。'),(r'\[.*\]\s*=','将编号与对应数据绑定；相同键会更新已有值。')],
'0.4':[(r'\.top\(|\.pop\(|\.pop_back\(','栈的最近加入项先离开；取出前必须确认非空。'),(r'\.front\(|popleft','队列的最早加入项先离开。')],
'0.5':[(r'priority_queue|heappush|heapify','最小堆先处理较小代价；C++的比较器方向与默认大根堆不同。')],
'1.1':[(r'while','闭区间只剩一个位置时仍需检查，所以条件包含相等。'),(r'left\s*=\s*mid\s*\+','中点已确认太小，连同它一起排除，边界必须真正前进。'),(r'right\s*=\s*mid\s*-','中点已确认太大，后续不再重复检查它。'),(r'mid\s*=','用左端加一半区间长度求中点，避免直接相加的溢出风险。')],
'1.2':[(r'while','本课使用左闭右开区间；左右相等时已经没有候选元素。'),(r'right\s*=\s*mid','当前值不小于目标，保留中点作为潜在插入边界。'),(r'return left','返回边界，允许等于长度；不要直接读取这个位置的元素。')],
'1.3':[(r'while','左右必须是不同位置，不能把同一个元素使用两次。'),(r'\+\+left|left\s*\+=|\+\+l\b','和偏小，排除当前最小候选；有序性保证不会漏掉正确配对。'),(r'--right|right\s*-=|--r\b','和偏大，排除当前最大候选。')],
'1.4':[(r'empty|not nums','先处理空输入，避免读取第一个元素。'),(r'nums\[.*slow.*\]\s*=','发现新值时才写入有效前缀，末尾旧内容无需清空。')],
'1.5':[(r'!=\s*val|!=\s*target','只有不等于待移除值的元素才保留，重复的有效值仍需保留。'),(r'nums\[.*slow.*\]\s*=','把有效值覆盖到下一个写入位置，不在遍历中反复erase。')],
'1.6':[(r'while.*(sum|total)','只要仍达到目标就继续收缩；只缩一次可能漏掉更短答案。'),(r'sum.*-=|total.*-=','左端离开窗口前先扣掉它的积分，再移动左边界。'),(r'best\s*=|answer\s*=|ans\s*=','用当前合法窗口更新最短长度；长度包含左右两端。')],
'1.7':[(r'left\s*=\s*(max|std::max)','左边界只能前进，不能被窗口外的旧出现位置拉回。'),(r'last\[.*\]\s*=','每轮更新字符最后一次出现的位置，供下一次重复判断。')],
'1.8':[(r'while','把比待插入值大的元素向后挪；相等时不挪，保留稳定性。'),(r'value\s*=|key\s*=','先保存待插入值，防止移动数组时覆盖它。')],
'2.1':[(r'if.*(n\s*==\s*0|n\s*<=\s*0)','基例直接返回，不再调用自己；这是递归能够结束的原因。'),(r'(sum|sum_to)\(n\s*-\s*1','把任务缩小一层，等它返回后再加上本层。')],
'2.2':[(r'smaller|partial','此处调用下一层时，本层会暂停，局部参数仍保存在调用栈中。'),(r'return','下层结果回来后，才计算本层并继续向上一层返回。')],
'2.3':[(r'left|right','这里只记录父子关系；空孩子表示对应方向没有节点。'),(r'delete','释放由new创建的节点，避免示例造成内存泄漏。')],
'2.4':[(r'push_back|append','有向边只表示从当前起点到终点；不自动添加反向通路。')],
'2.5':[(r'push_back|append','无向边需要在两个节点的邻居表中各存一次。')],
'2.6':[(r'visited.*true|visited.*True','发现时先标记，避免多个邻居把同一个节点重复入队。')],
'3.1':[(r'seen.*true|seen.*True','进入节点立即标记，环上的边就不会造成无限递归。'),(r'if.*!seen|if not seen','只沿尚未发现的邻居继续深入。')],
'3.2':[(r'rbegin|reversed','栈后进先出；想先访问的邻居应后压入。'),(r'seen.*true|seen.*True','压栈时标记，避免同一节点重复加入待处理栈。')],
'3.3':[(r'push_back|path\.append','把当前位置加入当前路线，不代表永久禁止其他路径使用它。'),(r'pop_back|path\.pop|onPath.*false|on_path.*False','返回上一层时恢复现场，让兄弟分支可以独立探索。'),(r'answer.*push|result.*append|paths.*append','保存路线副本，而不是继续变化的同一个容器引用。')],
'3.4':[(r'\.front\(|popleft','取最早发现的节点，保持逐层扩展顺序。'),(r'seen.*true|seen.*True','入队前标记，一个节点只加入一次。')],
'3.5':[(r'width\s*=|size\s*=|len\(q','每层先保存队列当前长度，只处理这一层原有节点。')],
'3.6':[(r'parent\[|prev\[','第一次发现时保存前驱，最后通过前驱链恢复真实路线。'),(r'reverse','回溯顺序是终点到起点，反转后才是执行方向。')],
'3.7':[(r'<\s*0|>=|0\s*<=','先检查坐标合法，再检查障碍与访问状态，防止越界。'),(r'return true|return True','找到一条路线即返回成功；这不保证它是最短路线。')],
'3.8':[(r'parent\[','保存发现当前格的上一格，用于恢复最短路径。'),(r'dist.*\+\s*1','四邻域每走一步代价相同，距离比父格多1。')],
'4.1':[(r'answer\.push_back|answer\.append','立即保存当前选择的副本，包含什么也不选的空集。'),(r'visit\(i\s*\+\s*1','只从后续下标选择，避免同一个组合换顺序后重复输出。'),(r'path\.pop','撤销本轮选择，恢复进入分支前的状态。')],
'4.2':[(r'lastEnd|end_time','保存上一个已选择任务的结束时刻，后面的任务不能与它冲突。'),(r'sort\(|sorted\(','按结束时间而非开始时间、时长排序。')],
'4.3':[(r'<=.*nums|a\[i\]\s*<=','相等时优先取左边，保持相等元素的相对顺序。'),(r'copy\(|a\[left:right\]','合并完成后写回对应区间，左右子问题的有序结果才能变成整段有序。')],
'4.4':[(r'dp\[0\]\s*=','到0级时什么也不做，是一种完整方案。'),(r'dp\[i\]\s*=','按最后一步来自前一级或前两级分类，不会重复计数。')],
'4.5':[(r'for.*capacity|range\(capacity','容量必须倒序，确保当前物品最多使用一次。'),(r'dp\[.*\].*=.*max','比较不选当前物品与选一次后的总价值，保留较好结果。')],
'4.6':[(r'for.*i\s*=\s*1|range\(1,\s*m','第0行、0列表示空前缀，所以真实字符从下标i−1、j−1读取。'),(r'reverse|reversed','回溯收集的是倒序公共字符，输出前需要反转。')],
'5.1':[(r'groups.*push|groups.*append','为本次搜索新建一个连通分量，孤立点也会形成一组。'),(r'if.*visited\[start\]|if start in seen','已经归类的节点无需重复发起搜索。')],
'5.2':[(r'cost\s*!=|distance\[u\].*!=','旧堆记录可能还在，但距离已经改善；过期记录直接跳过。'),(r'candidate.*<|cost\s*\+\s*weight\s*<','只有严格更短的路线才松弛，避免零权边反复制造重复记录。')],
'5.3':[(r'heuristic|h\s*=','四邻域单位步长使用曼哈顿距离作为剩余代价下界；h=0退化为一致代价搜索。'),(r'parent\[','只在路线改善时更新前驱，恢复时才有完整可行的父链。')],
'5.4':[(r'for.*k\s*=|for k in','中转点必须在最外层，表示本轮新允许使用哪个中转点。'),(r'distance\[i\]\[k\].*INF','两段都可达时才相加，避免把无穷大标记参与整数运算。')],
'5.5':[(r'--indegree|indegree\[.*\]\s*-=','完成当前任务后，后继少一个未满足依赖；恰好减到0才入队。'),(r'order\.size\(\).*graph\.size|len\(order\).*len\(graph\)','未能处理全部顶点意味着存在依赖环，不能把部分顺序当完整答案。')],
'5.6':[(r'parent\[u\]\s*=|self\.parent\[u\]\s*=','路径减半只让节点更接近同一个根，不改变它所属集合。'),(r'if.*a\s*==\s*b','两点已经同组，不再减少集合数量。')],
'5.7':[(r'sort\(|sorted\(','边按权重从小到大考虑；这里元组第一个字段就是权重。'),(r'if.*unite|if.*take','只连接原本不同的集合，保证选择过程不成环。')],
'6.1':[(r'heuristic|h\s*=','先明确格子、移动方向与代价单位，再选择与之匹配的启发式。'),(r'parent\[','探索区域不是最终路径；恢复时只沿前驱链取出一条路线。')],
'6.2':[(r'rhs\[goal\]|self\.rhs.*goal','目标的一跳前瞻代价固定为0，其余未建立的状态视为无穷大。'),(r'pending.*erase|pending\.pop','删除当前有效队列登记；堆中的历史副本由top惰性丢弃。'),(r'old\s*<','起点移动后关键字可能变大，先重新计算并按新键入队。'),(r'g\[u\]\s*=\s*INF|self\.g\[u\]\s*=\s*math.inf','旧代价失效时先设为无穷大，再重新传播，不直接把坏状态当作有效答案。'),(r'km\s*\+=|self\.km\s*\+=','移动起点时累加启发式偏移，复用原队列和搜索状态。'),(r'update\(u\)|self\.update\(u\)','重新检查当前顶点是否一致；不一致才进入修复队列。')],
'6.3':[(r'ratio\s*=|scale\s*=','单次扩展最多走一个步长，不直接跳到远处样本。'),(r'low\s*<=\s*high','线段参数与矩形在两个坐标轴的区间有公共部分，就发生碰撞。')],
'6.4':[(r'radius\s*=','二维邻域半径随有效样本数收缩，演示常数不直接等于理论保证。'),(r'parent\[j\]\s*=|parents\[j\]\s*=','只有经新节点严格更便宜且线段无碰撞，才重连旧节点。'),(r'while.*changed|while.*queue','把重连造成的成本变化传给全部后代，不能只改一个父指针。')],
'6.5':[(r'tau\s*=','把物理时间转换为0到1的归一化时间；求导后仍需除以实际时长。'),(r'velocity\s*=|double v\s*=','一次时间导数带1/T，得到米每秒。'),(r'acceleration\s*=|double a\s*=','二次时间导数带1/T²，得到米每二次方秒。')],
}

FUNCTION_COMMENTS={
'main':'程序入口：准备示例数据，调用算法，并输出结果供手算核对。',
'search':'在有序数组的闭区间内查找目标，找到返回下标，找不到返回−1。',
'searchInsert':'寻找第一个不小于目标的位置；允许返回数组长度作为末尾插入位置。',
'findIndex':'从哈希表查询键对应的下标，不存在时返回−1，不修改原表。',
'makeValues':'建立一个小型动态数组并返回，演示追加元素与按下标遍历。',
'twoSum':'在有序数组上用相向指针寻找两个不同位置，使其和值等于目标。',
'removeDuplicates':'把有序数组中的不同值写入有效前缀，并返回有效元素数量。',
'removeElement':'保留不等于指定值的元素，返回覆盖写入后的有效长度。',
'minSubArrayLen':'正整数条件下移动窗口，寻找达到目标和的最短连续区间。',
'sum_to':'先计算更小的前缀和，等待它返回后再加上当前数字。',
'sumTo':'先计算更小的前缀和，等待它返回后再加上当前数字。',
'__init__':'初始化本对象保存的状态，后续方法将共同使用这些成员。',
'h':'计算两格之间的曼哈顿距离，作为一致的剩余代价下界。',
'value':'读取状态表；尚未建立记录的顶点统一视为无穷大。',
'key':'计算两个字段组成的关键字，先比较第一项，相等时再比较第二项。',
'neighbors':'枚举地图内的四个相邻格；是否能穿过障碍由边代价函数进一步决定。',
'cost':'任一端点是障碍时边代价为无穷大，否则四邻域一步代价为1。',
'push':'登记顶点当前有效关键字并压入最小堆，旧副本暂时保留。',
'top':'在查看堆顶前丢弃过期副本，只返回当前有效的最小关键字。',
'update':'重新计算一跳前瞻代价；只有g与rhs不一致的顶点才需要进入修复队列。',
'repair':'传播不一致状态，直到当前位置一致，且队列没有更小关键字需要处理。',
'change':'修改一个格子的占据状态，并更新它及相邻格受影响的边代价。',
'move':'起点移动后维护关键字偏移km，保留并复用原有搜索数据。',
'moveStart':'起点移动后维护关键字偏移km，保留并复用原有搜索数据。',
'path':'沿边代价加后继g最小的方向提取路线，检测无路与异常循环。',
'subsets':'枚举当前路径和所有后续扩展，返回每个合法子集的一份独立副本。',
'select_intervals':'按结束时间从早到晚考虑活动，返回互不重叠的最大数量活动列表。',
'selectIntervals':'按结束时间从早到晚考虑活动，返回互不重叠的最大数量活动列表。',
'merge_sort':'用左右子问题分别排好序，再合并；返回新的有序列表。',
'mergeSort':'用一份共享辅助数组合并左右有序子段，原地更新原数组内容。',
'climb_stairs':'保存到达每级台阶的方案数，后续状态只依赖前两级的结果。',
'climbStairs':'保存到达每级台阶的方案数；输入上限用于防止long long溢出。',
'knapsack':'每件物品最多使用一次，对各容量比较不选与选一次的最大价值。',
'lcs':'填公共前缀状态表，再沿最优邻格回溯出一个最长公共子序列。',
'components':'从每个尚未归类的节点发起搜索，输出无向图的各个连通分量。',
'dijkstra':'非负权条件下优先处理当前最小有效距离，返回距离表与前驱表。',
'grid_astar':'在单位四邻域地图上搜索；h取曼哈顿距离，或取0进行一致代价搜索。',
'astar':'按已走代价加剩余下界选择扩展顺序，终点有效出队后恢复路径。',
'floyd_warshall':'逐轮开放中转点，计算全点对最短路，并检查是否存在负环。',
'floyd':'逐轮开放中转点，只有两段均可达时才尝试更新距离。',
'topological_sort':'持续处理没有剩余前置依赖的任务；处理不完全部任务就报告有向环。',
'topologicalSort':'持续处理没有剩余前置依赖的任务；处理不完全部任务就报告有向环。',
'find':'沿父指针找到集合代表，并压缩走过的路径以加速以后查询。',
'union':'只合并不同根代表的集合，并维护根的大小与当前分量数量。',
'unite':'只合并不同根代表的集合，并维护根的大小与当前分量数量。',
'kruskal':'按权重考虑边，利用并查集只连接不同分量，返回树或森林及总成本。',
'collision_free':'用线段参数区间检测闭矩形碰撞；接触障碍边界也视为碰撞。',
'collisionFree':'用线段参数区间检测闭矩形碰撞；接触障碍边界也视为碰撞。',
'distance':'计算两点的欧氏距离，与采样空间坐标使用相同长度单位。',
'rrt':'在连续空间采样、扩展与检测碰撞；启用star时增加邻域选父和重连。',
'plan':'在连续空间采样、扩展与检测碰撞；启用star时增加邻域选父和重连。',
'trajectory':'按物理时刻求五次位移曲线及其一、二阶时间导数。',
'quintic_trajectory':'对满足静止边界条件的五次多项式采样，返回时间、位置、速度、加速度。',
}

COMMON=[
(r'\bint main\(|^def main\(','程序入口：下面给出一组完整示例数据，可修改输入后重新运行。'),
(r'^class |^struct ','把相关数据与操作集中在一个类型中，避免混淆节点、状态与算法对象。'),
(r'if.*empty\(|if not \w+:','先处理空容器或无结果情况，避免访问不存在的元素。'),
(r'raise ValueError|throw invalid_argument','不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。'),
(r'\bparent\b.*-1|parents.*\[-1\]','没有前驱的起点用−1标记，回溯到这里就结束。'),
(r'\bvisited\b.*false|\bseen\b.*false|\bseen\b.*set\(','访问标记初始为空或全为假，表示还没有发现节点。'),
(r'while.*pending|while.*heap|while.*ready|while.*queue|while.*stack','反复取出一个待处理状态；集合耗尽时，本轮搜索结束。'),
(r'heapq\.heappop|heap\.pop\(','处理优先级最高的当前记录；是否仍有效要结合后面的条件判断。'),
(r'heapq\.heappush|heap\.push\(','加入新的候选状态；允许旧记录留在堆中，由出队检查负责丢弃。'),
(r'\.popleft\(|\.front\(','读取先进先出的队首，保持发现的层次顺序。'),
(r'\.reverse\(|reverse\(|reversed\(','把反向收集的数据恢复为实际输出顺序。'),
(r'\bprint\(|\bcout\b','输出计算结果，便于与课程例子或自行推演的答案核对。'),
]

def strip_cpp_literals(source):
    return re.sub(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', ' ', source)

def required_headers(source):
    body=re.sub(r'^#include[^\n]*\n','',source,flags=re.M)
    symbols=strip_cpp_literals(body)
    return [name for name,(pattern,_) in HEADERS.items() if re.search(pattern,symbols)]

def annotate_lines(id,source,language):
    prefix='// ' if language=='cpp' else '# '
    lines=[];last_note=None
    rules=NOTES.get(id,[])+COMMON
    for raw in source.splitlines():
        raw=raw.rstrip()
        stripped=raw.strip()
        if language=='cpp' and stripped.startswith('//'):continue
        if language=='python' and stripped.startswith('#'):continue
        if not stripped:lines.append(raw);last_note=None;continue
        if language=='cpp' and stripped.startswith(('#include','using namespace')):
            lines.append(raw);continue
        if language=='python' and stripped.startswith(('import ','from ','"""')):
            lines.append(raw);continue
        function=re.match(r'def\s+(\w+)\(',stripped) if language=='python' else re.match(r'(?:[\w:<>,*&]+ )+([\w:~]+)\([^;]*\)\s*(?:const\s*)?\{',stripped)
        if function:
            name=function[1]
            note=FUNCTION_COMMENTS.get(name)
            if id=='6.3' and name in ('rrt','plan'):
                note='随机采样并向最近节点扩展，只保留整段无碰撞的连接；返回采样树与找到的路径。'
            if name in ('dfs','visit'):
                note='在当前分支中选择并递归探索，返回后恢复现场。' if id in ('3.3','4.1') else '进入节点后标记，再逐个递归访问尚未发现的邻居。'
            if note:
                lines.append(raw[:len(raw)-len(raw.lstrip())]+prefix+note)
                lines.append(raw);last_note=note;continue
        # Avoid filling every adjacent output/loop line with the same comment.
        for pattern,note in rules:
            if re.search(pattern,stripped):
                if note!=last_note:
                    lines.append(raw[:len(raw)-len(raw.lstrip())]+prefix+note)
                    last_note=note
                break
        lines.append(raw)
    return '\n'.join(lines)+'\n'

class RemovePresentation(ast.NodeTransformer):
    def visit_Expr(self,node):
        if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='emit_state':return None
        if isinstance(node.value,ast.Constant) and isinstance(node.value.value,str):
            translations={'Four-connected undirected grid; lazy deletion of obsolete queue entries.':'四邻域无向栅格；保留g/rhs，采用惰性删除过滤过期队列项。',
                          'Segment against closed axis-aligned rectangles using slab intersection.':'通过线段参数区间求交检测闭矩形障碍；边界接触也算碰撞。'}
            node.value.value=translations.get(node.value.value,node.value.value)
        return self.generic_visit(node)
    def visit_FunctionDef(self,node):
        if node.name in ('emit_state','scores'):return None
        node=self.generic_visit(node)
        arguments=node.args.args
        default_start=len(arguments)-len(node.args.defaults)
        defaults={arg.arg:node.args.defaults[i-default_start] for i,arg in enumerate(arguments) if i>=default_start}
        node.args.args=[arg for arg in arguments if arg.arg!='emit']
        node.args.defaults=[defaults[arg.arg] for arg in node.args.args if arg.arg in defaults]
        return node

class BasicRRT(ast.NodeTransformer):
    """The RRT lesson should not introduce RRT* rewiring before the next lesson."""
    def visit_FunctionDef(self,node):
        if node.name=='rrt':
            arguments=node.args.args;start=len(arguments)-len(node.args.defaults)
            defaults={arg.arg:node.args.defaults[i-start] for i,arg in enumerate(arguments) if i>=start}
            node.args.args=[arg for arg in arguments if arg.arg!='star']
            node.args.defaults=[defaults[arg.arg] for arg in node.args.args if arg.arg in defaults]
        return self.generic_visit(node)
    def visit_If(self,node):
        if isinstance(node.test,ast.Name) and node.test.id=='star':return [self.visit(child) for child in node.orelse]
        return self.generic_visit(node)
    def visit_IfExp(self,node):
        if isinstance(node.test,ast.Name) and node.test.id=='star':return self.visit(node.orelse)
        return self.generic_visit(node)
    def visit_Assign(self,node):
        if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in ('radius','neighbors','feasible','rewired'):return None
            if name=='parent':node.value=ast.Name(id='near',ctx=ast.Load())
        return self.generic_visit(node)
    def visit_Call(self,node):
        if isinstance(node.func,ast.Name) and node.func.id=='rrt' and node.args and isinstance(node.args[-1],ast.Constant) and node.args[-1].value is False:node.args.pop()
        return self.generic_visit(node)

def clean_python(source,id):
    tree=ast.parse(source)
    tree=RemovePresentation().visit(tree);ast.fix_missing_locations(tree)
    if id=='6.3':tree=BasicRRT().visit(tree);ast.fix_missing_locations(tree)
    names={node.id for node in ast.walk(tree) if isinstance(node,ast.Name)}
    for node in tree.body[:]:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            node.names=[alias for alias in node.names if (alias.asname or alias.name.split('.')[0]) in names]
            if not node.names:tree.body.remove(node)
        elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str):
            tree.body.remove(node)
    return ast.unparse(tree)+'\n'

def prepare(id,title,cpp,python):
    if id=='6.3':
        begin=cpp.index('        double radius =')
        end=cpp.index('        tree.points.push_back(point);',begin)
        cpp=cpp[:begin]+'        int parent = near;\n'+cpp[end:]
        begin=cpp.index('        for (int j : neighbors) {')
        end=cpp.index('        if (distance(point,goal)',begin)
        cpp=cpp[:begin]+cpp[end:]
        cpp=cpp.replace(', bool star) {',') {').replace(',7,false);',',7);')
    includes=required_headers(cpp)
    body=re.sub(r'^#include[^\n]*\n','',cpp,flags=re.M).lstrip()
    body=re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*',lambda m:'' if m[0].startswith('//') else m[0],body)
    heading=['// '+title,'// 学习重点：'+FLOW[id][2][0], '// '+FLOW[id][2][1], '// '+FLOW[id][2][2], '// C++17；直接编译运行 main() 中的示例。','']
    header=''.join('#include <'+name+'>  // '+HEADERS[name][1]+'\n' for name in includes)+'\n'
    cpp='\n'.join(heading)+header+annotate_lines(id,body,'cpp')
    python=clean_python(python,id)
    python='# '+title+'\n# Python 3；直接运行文件，修改示例数据可继续练习。\n# '+FLOW[id][2][0]+'\n\n'+annotate_lines(id,python,'python')
    return cpp,python

def header_table(cpp):
    includes=re.findall(r'^#include <([^>]+)>',cpp,re.M)
    return '<div class="teaching-table"><table><thead><tr><th>本课头文件</th><th>为什么需要</th></tr></thead><tbody>'+''.join('<tr><td><code>&lt;'+name+'&gt;</code></td><td>'+escape(HEADERS[name][1])+'</td></tr>' for name in includes)+'</tbody></table></div>'
