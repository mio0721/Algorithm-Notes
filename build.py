from pathlib import Path
from html import escape
import json
import posixpath
from content import LESSONS
from code_examples import code_for
ROOT=Path(__file__).resolve().parent
DATA={x[0]:x for x in LESSONS}
PHASES=[
('阶段 0','算法基础与 C++ STL','穿插学习',[('0.1','算法与时间复杂度'),('0.2','vector 与数组'),('0.3','哈希表'),('0.4','栈与队列'),('0.5','堆与优先队列')]),
('阶段 1','数组、查找与双指针','数组、查找与指针技巧',[(f'1.{i}',name) for i,name in enumerate(['二分查找','二分边界与插入位置','相向双指针','快慢指针：数组去重','快慢指针：原地移除','滑动窗口：长度最小的子数组','滑动窗口与哈希表','排序算法'],1)]),
('阶段 2','递归、树与图的基础','递归、树和图的基本概念',[(f'2.{i}',name) for i,name in enumerate(['递归基础','函数调用栈与递归返回','树的基本结构','图的基本结构','图的存储：邻接表与邻接矩阵','visited 访问标记'],1)]),
('阶段 3','DFS 与 BFS 搜索算法','学习搜索算法与图遍历',[(f'3.{i}',name) for i,name in enumerate(['递归 DFS','非递归 DFS','DFS 与回溯','队列 BFS','树的层序遍历','无权图最短路径','二维地图 DFS','二维地图 BFS 与对比'],1)]),
('阶段 4','经典算法设计思想','课程规划',[(f'4.{i}',name) for i,name in enumerate(['回溯算法','贪心算法','分治算法','动态规划基础','背包动态规划','动态规划进阶'],1)]),
('阶段 5','图论与最短路径','课程规划',[(f'5.{i}',name) for i,name in enumerate(['图的遍历与连通性','Dijkstra','A*','Floyd–Warshall','拓扑排序','并查集','最小生成树'],1)]),
('阶段 6','机器人与自动驾驶规划算法','课程规划',[(f'6.{i}',name) for i,name in enumerate(['栅格地图搜索','动态重规划与 D* Lite','RRT','RRT*','轨迹规划基础'],1)]),
('阶段 7','算法面试与综合实战','课程规划',[(f'7.{i}',name) for i,name in enumerate(['常用 STL 综合训练','手写算法模拟面试','复杂度与边界分析','算法调试与测试','机器人地图搜索综合项目'],1)])]
def lesson_folder(id):
 name=next(name for _,_,_,items in PHASES for lesson_id,name in items if lesson_id==id)
 # Windows 文件名不能包含冒号、星号等字符，保留其余课程名称。
 import re
 name=re.sub(r'[\\/:*?"<>|]+','-',name).strip(' .-')
 return 'lesson-'+id.replace('.','-')+'-'+name
def url(id):return 'lessons/stage-'+id.split('.')[0]+'/'+lesson_folder(id).removeprefix('lesson-')+'.html'
def code_url(id):return 'codes/stage-'+id.split('.')[0]+'/'+lesson_folder(id).removeprefix('lesson-')+'.html'
def lesson_link(target,current):
 return posixpath.relpath(url(target),posixpath.dirname(url(current))) if current else url(target)
def status(id):return '已上线' if id in DATA else '待制作'
def sidebar(current,section='lesson'):
 home='../../index.html' if current else 'index.html'
 out=[f'<nav class="sidebar" aria-label="课程目录"><div class="sidebar-title">课程总目录</div><a class="nav-home" href="{home}">首页 · 课程目录</a><div class="group-label">按学习阶段查看</div>']
 for phase,title,note,items in PHASES:
  expanded=' open' if current and current.split('.')[0]==items[0][0].split('.')[0] else ''
  out.append(f'<details class="nav-phase"{expanded}><summary><span class="phase-title">{phase} · {escape(title)}</span><small>{escape(note)}</small></summary>')
  for id,name in items:
   if id in DATA:
    course_open=' open' if id==current else ''
    active=' class="active"' if id==current and section=='lesson' else ''
    code_active=' class="active"' if id==current and section=='code' else ''
    source=code_url(current) if current and section=='code' else url(current) if current else None
    link=lambda target:posixpath.relpath(target,posixpath.dirname(source)) if source else target
    out.append(f'<details class="nav-course"{course_open}><summary><span class="course-number">{id}</span><span class="course-title">{escape(name)}</span></summary><div class="nav-course-links"><a{active} href="{link(url(id))}">课程内容</a><a{code_active} href="{link(code_url(id))}">完整代码</a></div></details>')
   else:out.append(f'<div class="nav-course unavailable"><span class="course-number">{id}</span><span>{escape(name)} · 待制作</span></div>')
  out.append('</details>')
 out.append('</nav>');return ''.join(out)
def page(title,main,current=None,problem=None,section='lesson'):
 rail=(f'<aside class="problem-rail" aria-label="本节题目">{problem}</aside>' if problem else '')
 layout_class='layout has-problem' if problem else 'layout'
 prefix='../../' if current else ''
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · 算法笔记</title><script>try{{document.documentElement.dataset.theme=localStorage.getItem('algorithm-notes-theme')||'light'}}catch(e){{}}</script><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/traces.js"></script><script defer src="{prefix}assets/app.js"></script></head><body><header class="mast"><div class="mast-inner"><a class="brand" href="{prefix}index.html">算法与数据结构：从基础到机器人路径规划</a><button class="theme theme-toggle" id="theme-toggle" type="button" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">夜间模式</span></button></div></header><div class="{layout_class}">{sidebar(current,section)}<main class="main">{main}</main>{rail}</div></body></html>'''
def lesson_page(item):
 id,title,problem,intuition,rules,complexity,frames,code,exercise,hint=item
 frame_data=[{'cells':cells,'text':text,'active':active} for cells,text,active in frames]
 raw=json.dumps(frame_data,ensure_ascii=False).replace('<','\\u003c')
 nav_ids=list(DATA);i=nav_ids.index(id)
 originals={'1.1':'01_二分查找_LeetCode704.html','1.2':'02_搜索插入位置_LeetCode35.html','1.3':'03_两数之和II_LeetCode167.html','1.4':'04_删除有序数组重复项_LeetCode26.html','1.5':'05_移除元素_LeetCode27.html','1.6':'06_长度最小的子数组_LeetCode209.html'}
 interactive=id in originals
 controls=("<div class=\"demo-controls\"><label>输入数组（整数，逗号或空格分隔）<input type=\"text\" data-input=\"array\" placeholder=\"留空表示空数组\"></label>"+("<label>"+('需要移除的值' if id=='1.5' else '目标值')+"<input type=\"number\" step=\"1\" data-input=\"target\"></label>" if id!='1.4' else '')+"<label>预设例子<select data-input=\"preset\"><option value=\"default\">默认例子</option><option value=\"first\">首端情况</option><option value=\"last\">末端情况</option><option value=\"single\">单元素</option><option value=\"empty\">空数组（扩展）</option><option value=\"missing\">无解或重复情况</option></select></label><button type=\"button\" data-action=\"apply\">应用输入并演示</button><p class=\"demo-error\" role=\"alert\"></p></div>") if interactive else ''
 explanation='可修改数组与目标；逐步观察指针、当前比较位置和有效区间。浅色方格表示当前区间或已保留前缀，淡化的方格表示区间之外。' if interactive else '这是一个固定例子。先猜测下一步，再点击按钮；高亮表示当前关注的元素或状态。'
 play='<button type="button" data-action="play">自动播放</button>'
 legacy=''
 copy='<button type="button" class="copy-code" data-copy aria-label="复制代码" title="复制代码"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="8" y="8" width="11" height="12" rx="2"></rect><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h2"></path></svg></button><span class="copy-status" role="status" aria-live="polite"></span>'

 prev=f'<a href="{lesson_link(nav_ids[i-1],id)}">← 上一节</a>' if i else '<a href="../../index.html">← 课程目录</a>'
 nxt=f'<a href="{lesson_link(nav_ids[i+1],id)}">下一节 →</a>' if i+1<len(nav_ids) else '<a href="../../index.html">回到课程目录 →</a>'
 return f'''<div class="eyebrow">阶段 {id.split('.')[0]} · 第 {id} 节</div><h1>{escape(title)}</h1><span class="tag">{escape(problem)}</span><div class="lead"><strong>这一节要解决什么？</strong><p>{escape(intuition)}</p></div><h2>一、先理解做法</h2><p>{escape(rules)}</p><h2>二、逐步观察</h2><p>{explanation}</p><div class="demo" data-lesson="{id}" aria-label="逐步演示">{controls}<div class="graph-view"></div><div class="stage" aria-live="polite"></div><div class="pointer-outside" aria-live="polite"></div><p class="step-text" aria-live="polite"></p><div class="buttons"><button type="button" data-action="prev">上一步</button><button type="button" data-action="next">下一步</button><button type="button" data-action="reset">重新开始</button>{play}</div><div class="status"></div></div><script id="lesson-frames" type="application/json">{raw}</script><h2>三、C++ 实现</h2><p>先读参数与返回值，再逐行对照上面的状态变化。标准容器写法假定已引入相应头文件并使用 <code>std</code> 命名空间；结构定义和片段按上下文放入程序。</p><div class="code-block">{copy}<pre><code class="language-cpp">{escape(code)}</code></pre></div><h2>四、复杂度与适用条件</h2><p>{escape(complexity)}</p><h2>五、独立练习</h2><p>{escape(exercise)}</p><details class="answer"><summary>查看提示与易错点</summary><p>{escape(hint)}</p></details><h2>六、完成前自查</h2><ol><li>能不看代码描述变量的含义和每一步变化吗？</li><li>能解释循环或递归何时结束，以及空输入、边界情况如何处理吗？</li><li>能独立复写，并解释时间与额外空间复杂度吗？</li></ol>{legacy}<div class="next">{prev}{nxt}</div>'''
PROBLEMS={
'1.1':('704. 二分查找','给定升序且元素互不相同的整数数组 nums 和整数 target，找到目标并返回其下标；找不到则返回 -1。要求时间复杂度 O(log n)。',[('nums = [-1,0,3,5,9,12], target = 9','4'),('nums = [-1,0,3,5,9,12], target = 2','-1')],'原题数组非空、元素互不相同。空数组预设用于扩展边界练习。','https://leetcode.cn/problems/binary-search/'),
'1.2':('35. 搜索插入位置','给定由互不相同的整数组成的升序数组和目标值，找到目标时返回其下标；不存在时返回应插入的位置，以保持有序。要求时间复杂度 O(log n)。',[('nums = [1,3,5,6], target = 5','2'),('nums = [1,3,5,6], target = 2','1')],'原题数组非空、元素互不相同。空数组与重复元素可作为扩展思考；本实现返回第一个不小于目标的位置。','https://leetcode.cn/problems/search-insert-position/'),
'1.3':('167. 两数之和 II','给定非递减数组，找到两个不同元素，使它们之和等于目标值，返回两个下标；原题的下标从 1 开始。',[('numbers = [2,7,11,15], target = 9','[1,2]')],'原题保证恰有一个解，且不能重复使用同一元素。无解预设是扩展练习。','https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/'),
'1.4':('26. 删除有序数组中的重复项','给定非递减整数数组，原地把不重复的元素放在前面并保持顺序，返回不同元素个数 k。只需保证前 k 个元素是结果。',[('nums = [0,0,1,1,2]','k = 3，前 3 项为 [0,1,2]')],'原题数组至少有一个元素；空数组是扩展边界。本课返回后面的剩余内容不作要求。','https://leetcode.cn/problems/remove-duplicates-from-sorted-array/'),
'1.5':('27. 移除元素','给定整数数组 nums 和值 val，原地移除所有等于 val 的元素，返回剩余元素个数 k；结果写在前 k 个位置。',[('nums = [3,2,2,3], val = 3','k = 2，前 2 项为 [2,2]')],'本课实现保持剩余元素相对顺序；原题允许改变顺序。','https://leetcode.cn/problems/remove-element/'),
'1.6':('209. 长度最小的子数组','给定由正整数组成的数组和正整数 target，找到和大于或等于 target 的最短连续子数组，返回其长度；不存在则返回 0。',[('target = 7, nums = [2,3,1,2,4,3]','2，对应 [4,3]')],'原题数组非空、元素和 target 均为正整数；空数组在此作为扩展边界练习。','https://leetcode.cn/problems/minimum-size-subarray-sum/')}

LIMITS={
'1.1':'1 ≤ 数组长度 ≤ 10⁴；元素和目标均大于 -10⁴ 且小于 10⁴。',
'1.2':'1 ≤ 数组长度 ≤ 10⁴；元素与目标均在 [-10⁴,10⁴] 内。',
'1.3':'2 ≤ 数组长度 ≤ 3×10⁴；元素与目标均在 [-1000,1000] 内。',
'1.4':'1 ≤ 数组长度 ≤ 3×10⁴；元素在 [-100,100] 内。',
'1.5':'0 ≤ 数组长度 ≤ 100；元素在 [0,50] 内，val 在 [0,100] 内。',
'1.6':'1 ≤ target ≤ 10⁹；1 ≤ 数组长度 ≤ 10⁵；元素在 [1,10⁴] 内。'}

def problem_panel(item):
 id,title,_,_,_,complexity,_,_,exercise,_=item
 if id not in PROBLEMS:
  return '<h2>本节练习</h2><p>'+escape(exercise)+'</p><h3>检查重点</h3><p>'+escape(complexity)+'</p><p class="muted">先独立思考，再回正文展开提示。</p>'
 name,description,examples,limits,link=PROBLEMS[id]
 ex=''.join('<div class="problem-example"><strong>输入</strong><code>'+escape(a)+'</code><strong>输出</strong><code>'+escape(b)+'</code></div>' for a,b in examples)
 return '<h2>本题题目</h2><p><strong>'+escape(name)+'</strong></p><p>'+escape(description)+'</p><h3>输入 / 输出示例</h3>'+ex+'<h3>条件与边界</h3><p>'+escape(limits)+' '+escape(LIMITS[id])+'</p><p class="muted">演示区为方便观察最多接受 20 个数，数值绝对值不超过 1000000；实际题目以这里的限制为准。</p><p><a href="'+link+'" target="_blank" rel="noopener noreferrer">查看力扣原题 ↗</a></p>'

def main():
 (ROOT/'codes').mkdir(exist_ok=True)
 for phase,title,note,items in PHASES:
  stage=items[0][0].split('.')[0]
  (ROOT/'lessons'/('stage-'+stage)).mkdir(parents=True,exist_ok=True)
 for item in LESSONS:
  id=item[0]
  (ROOT/url(id)).parent.mkdir(parents=True,exist_ok=True)
  (ROOT/url(id)).write_text(page(item[1],lesson_page(item),id,problem_panel(item)),encoding='utf-8')
  cpp,python=code_for(item)
  folder=ROOT/'codes'/('stage-'+id.split('.')[0]);folder.mkdir(parents=True,exist_ok=True)
  filename=lesson_folder(id).removeprefix('lesson-')
  (folder/(filename+'.cpp')).write_text(cpp,encoding='utf-8')
  (folder/(filename+'.py')).write_text(python,encoding='utf-8')
  copy='<button type="button" class="copy-code" data-copy aria-label="复制代码" title="复制代码"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="8" y="8" width="11" height="12" rx="2"></rect><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h2"></path></svg></button><span class="copy-status" role="status" aria-live="polite"></span>'
  blocks=[]
  for name,lang,text,extension in [('C++','cpp',cpp,'cpp'),('Python','python',python,'py')]:
   codefile=filename+'.'+extension
   blocks.append(f'<h2>{name} 完整示例</h2><p><a href="{escape(codefile,quote=True)}" download>下载 {escape(codefile)}</a></p><div class="code-block">{copy}<pre><code class="language-{lang}">{escape(text)}</code></pre></div>')
  lesson_target=posixpath.relpath(url(id),posixpath.dirname(code_url(id)))
  main=f'<div class="eyebrow">第 {id} 课 · 完整代码</div><h1>{escape(item[1])}</h1><p>下面的程序包含示例数据，可直接复制运行；修改数据可继续练习。</p><p><a href="{lesson_target}">← 返回课程内容</a></p>'+''.join(blocks)
  (ROOT/code_url(id)).write_text(page(item[1]+' · 完整代码',main,id,section='code'),encoding='utf-8')
 main_html=['<div class="eyebrow">算法知识体系 · 机器人路径规划</div><h1>算法与数据结构：从基础到机器人路径规划</h1><p>先建立算法直觉和 C++ 实现能力，再通过题目与机器人场景练习。课程按知识体系组织，不完全按 LeetCode Hot 100 顺序。</p><h2>八个学习阶段</h2><p class="muted">课程共规划 50 节，阶段 0 的基础内容可结合后续课程学习。</p><div class="phases">']
 for phase,title,note,items in PHASES:
  main_html.append(f'<details class="phase"{" open" if phase=="阶段 2" else ""}><summary>{phase} · {escape(title)}　<small class="muted">{escape(note)}</small></summary><div class="phase-body">')
  for id,name in items:
   label=f'<a href="{url(id)}">{id} {escape(name)}</a>' if id in DATA else f'<span>{id} {escape(name)}</span>'
   main_html.append(f'<div class="phase-row">{label}<small>{status(id)}</small></div>')
  main_html.append('</div></details>')
 main_html.append('</div><h2>每课怎样学习？</h2><p>先理解场景，再逐步观察算法、阅读代码、独立完成练习，最后检查边界和复杂度。课程目录还提供可直接运行的 C++ 与 Python 示例。</p>')
 (ROOT/'index.html').write_text(page('课程首页',''.join(main_html)),encoding='utf-8')
 print(f'Built {len(LESSONS)} lessons and one course index.')
if __name__=='__main__':main()


