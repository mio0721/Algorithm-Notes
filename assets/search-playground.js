/* Editable graph and grid exercises. All computation stays in the page. */
(()=>{
'use strict';
const supported=['2.3','2.4','2.5','2.6','3.1','3.2','3.3','3.4','3.5','3.6','3.7','3.8'];
const tree=[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6],[3,7],[4,8],[6,9]];
const cyclic=[...tree,[4,5],[8,9]];
const graphCases={default:cyclic,tree,chain:Array.from({length:9},(_,i)=>[i,i+1]),disconnected:[[0,1],[1,2],[2,3],[4,5],[5,6],[6,7],[7,8],[8,9]],ring:Array.from({length:10},(_,i)=>[i,(i+1)%10]),single:[]};
const grids={default:'S...\n.##.\n...T',maze:'S......\n.#####.\n.....#.\n####.#.\n.....#T',blocked:'S..#...\n...#...\n...#..T',open:'S......\n.......\n.......\n......T',detour:'S.#...T\n..#.#..\n..#.#..\n....#..',single:'S.T'};
const label=n=>String.fromCharCode(65+n);
function graphData(count,text,start,goal,treeMode=false){
 if(!Number.isInteger(count)||count<1||count>12)throw Error('节点数应为 1～12。');
 const node=value=>{const s=String(value).trim().toUpperCase();const n=/^[A-L]$/.test(s)?s.charCodeAt(0)-65:/^\d+$/.test(s)?Number(s):NaN;if(!Number.isInteger(n)||n<0||n>=count)throw Error('节点必须在当前范围内，例如 A 或 0。');return n;};
 const edges=[],keys=new Set();
 for(const row of text.split(/[;；\n]+/).map(s=>s.trim()).filter(Boolean)){
  const parts=row.split(/[\s,，→>—-]+/).filter(Boolean);if(parts.length!==2)throw Error('每行输入一条边，例如 A B。');
  const a=node(parts[0]),b=node(parts[1]);if(a===b)throw Error('本练习不接受自环。');
  const key=a+','+b;if(!keys.has(key)){keys.add(key);edges.push([a,b]);}
 }
 const first=node(start),last=node(goal);
 if(treeMode){
  const p=Array.from({length:count},(_,i)=>i),find=x=>p[x]===x?x:p[x]=find(p[x]);
  for(const [a,b] of edges){const x=find(a),y=find(b);if(x===y)throw Error('树不能包含环或重复的无向边。');p[x]=y;}
  if(edges.length!==count-1)throw Error('树必须连通，并且恰好有节点数减一条边。');
 }
 return {count,edges,start:first,goal:last};
}
function layoutGraph(g,start){
 const count=g.length,children=Array.from({length:count},()=>[]),depth=Array(count).fill(-1),roots=[];
 // Build a rooted spanning forest. Additional graph edges remain visible.
 for(const root of [start,...Array.from({length:count},(_,i)=>i)]){
  if(depth[root]!==-1)continue;
  roots.push(root);depth[root]=0;const queue=[root];
  for(let head=0;head<queue.length;head++){
   const u=queue[head];
   for(const v of g[u])if(depth[v]===-1){depth[v]=depth[u]+1;children[u].push(v);queue.push(v);}
  }
 }
 const xs=Array(count).fill(0);let leaf=0;
 const place=u=>{if(!children[u].length)xs[u]=leaf++*70;else{children[u].forEach(place);xs[u]=(xs[children[u][0]]+xs[children[u].at(-1)])/2;}};
 roots.forEach(root=>{place(root);leaf+=0.5;});
 const min=Math.min(...xs),max=Math.max(...xs),width=Math.max(420,max-min+90),offset=(width-(max-min))/2-min;
 const positions=xs.map((x,u)=>[x+offset,40+depth[u]*76]);
 return {positions,viewBox:[0,0,width,Math.max(260,Math.max(...depth)*76+88)]};
}
function graphTrace(id,data){
 const {count,edges,start,goal}=data,directed=id==='2.4'||id==='3.3',g=Array.from({length:count},()=>[]);
 edges.forEach(([a,b])=>{g[a].push(b);if(!directed)g[b].push(a);});g.forEach(a=>a.sort((a,b)=>a-b));
 const {positions,viewBox}=layoutGraph(g,start);
 const diagram={nodes:positions.map(([x,y],i)=>[label(i),x,y]),edges,directed,viewBox};
 const frames=[],seen=new Set(),order=[],path=[];const show=a=>a.map(label).join(' → ')||'空';
 const add=(text,highlight=[],cells=[],partial=diagram)=>{if(frames.length<450)frames.push({text,highlight:[...highlight],cells:[...cells],active:[],diagram:partial});};
 add(`${count} 个节点；${directed?'有向':'无向'}图。从 ${label(start)} 出发。`,[],[],['2.4','2.5'].includes(id)?{...diagram,edges:[]}:diagram);
 if(id==='2.5'){
  const adj=Array.from({length:count},()=>[]);
  edges.forEach(([a,b],index)=>{adj[a].push(b);adj[b].push(a);add(`加入无向边 ${label(a)}—${label(b)}，两端邻接表都更新。`,[a,b],adj.map((v,u)=>`${label(u)}: ${show(v)}`),{...diagram,edges:edges.slice(0,index+1)});});
  return frames;
 }
 if(id==='2.4'){edges.forEach(([a,b],i)=>add(`加入 ${label(a)} → ${label(b)}；反向不自动成立。`,[a,b],[],{...diagram,edges:edges.slice(0,i+1)}));return frames;}
 if(id==='3.3'){
  let paths=0,truncated=false;const results=[];
  const dfs=u=>{if(frames.length>=440){truncated=true;return;}seen.add(u);path.push(u);add(`选择 ${label(u)}`,path,['当前路径：'+show(path)]);
   if(u===goal){paths++;results.push([...path]);add(`找到第 ${paths} 条路径。`,path,['结果：'+show(path)]);frames.at(-1).route=[...path];}
   else for(const v of g[u])if(!seen.has(v))dfs(v);
   path.pop();seen.delete(u);add(`撤销 ${label(u)}`,path,['当前路径：'+show(path)]);
  };dfs(start);add(truncated?`路径较多，演示已截取前 440 步；已找到 ${paths} 条路径。`:`结束，共找到 ${paths} 条简单路径。`,results[0]||[],[]);frames.at(-1).routes=results;return frames;
 }
 if(id==='3.1'||id==='2.6'){
  const dfs=u=>{seen.add(u);path.push(u);order.push(u);add(`进入 ${label(u)}，立即标记。`,[u],['调用栈：'+show(path),'访问顺序：'+show(order)]);for(const v of g[u])if(!seen.has(v))dfs(v);path.pop();add(`从 ${label(u)} 返回。`,path.slice(-1),['调用栈：'+show(path)]);};dfs(start);
 }else if(id==='3.2'){
  const stack=[start];seen.add(start);while(stack.length){const u=stack.pop();order.push(u);for(const v of [...g[u]].reverse())if(!seen.has(v)){seen.add(v);stack.push(v);}add(`处理 ${label(u)}；右端为栈顶。`,[u],['栈：'+show(stack),'访问顺序：'+show(order)]);}
 }else{
  const queue=[start],dist=Array(count).fill(-1),parent=Array(count).fill(-1);dist[start]=0;seen.add(start);let depth=0;
  while(queue.length){
   const size=(id==='3.5'||id==='2.3')?queue.length:1,layer=[];
   for(let i=0;i<size;i++){const u=queue.shift();order.push(u);layer.push(u);for(const v of g[u])if(!seen.has(v)){seen.add(v);dist[v]=dist[u]+1;parent[v]=u;queue.push(v);}}
   add(size===1?`处理 ${show(layer)}，距离 ${dist[layer[0]]}。`:`第 ${depth} 层：${show(layer)}`,layer,['队列：'+show(queue),'访问顺序：'+show(order)]);depth++;
  }
  if(id==='3.6'){
   if(dist[goal]<0)add(`${label(goal)} 不可达：没有路径。`);
   else{let u=goal;while(u!==-1){path.push(u);u=parent[u];}path.reverse();add(`最短路径 ${dist[goal]} 步。`,path,['路径：'+show(path)]);frames.at(-1).route=[...path];}return frames;
  }
 }
 add(`本次访问 ${seen.size}/${count} 个节点。${seen.size<count?'其他节点从当前起点不可达。':'所有节点均可达。'}`,[],['访问顺序：'+show(order)]);return frames;
}
function parseGrid(text){
 const rows=text.trim().split(/\r?\n/).map(r=>r.trim());
 if(!rows.length||rows.length>12||!rows[0].length||rows[0].length>12||rows.some(r=>r.length!==rows[0].length))throw Error('请输入矩形地图，最大 12 行、12 列。');
 let start,goal;
 rows.forEach((row,r)=>[...row].forEach((x,c)=>{if(!'.#ST'.includes(x))throw Error('地图只能使用 . # S T。');if(x==='S'){if(start)throw Error('只能有一个起点 S。');start=[r,c];}if(x==='T'){if(goal)throw Error('只能有一个终点 T。');goal=[r,c];}}));
 if(!start||!goal)throw Error('请设置一个起点 S 和一个终点 T。');
 return {grid:rows.map(r=>r.replace(/[ST]/g,'.')),start,goal};
}
function gridTrace(id,data){
 const {grid,start,goal}=data,R=grid.length,C=grid[0].length,frames=[],seen=new Set(),pending=[],path=[],dist={},parent={};
 const key=p=>p.join(','),eq=(a,b)=>key(a)===key(b),cells=()=>[...seen].map(k=>k.split(',').map(Number));
 const add=(text,current=null,route=[])=>frames.push({text,cells:[],active:[],grid,start,goal,visited:cells(),current,route:route.map(p=>[...p]),frontier:pending.map(p=>[...p]),distances:{...dist}});
 const neighbors=([r,c])=>[[r+1,c],[r-1,c],[r,c+1],[r,c-1]].filter(([r,c])=>r>=0&&r<R&&c>=0&&c<C&&grid[r][c]!=='#');
 add('S 为起点、T 为终点。点击格子可以编辑地图，再观察搜索过程。');
 if(id==='3.7'){
  const dfs=p=>{seen.add(key(p));path.push(p);add(`进入 (${p})`,p,path);if(eq(p,goal)){add(`找到一条 ${path.length-1} 步的路径；DFS 不保证最短。`,p,path);return true;}for(const v of neighbors(p))if(!seen.has(key(v))&&dfs(v))return true;path.pop();add(`从 (${p}) 回退。`,path.at(-1)||null,path);return false;};
  if(!dfs(start))add('搜索结束：终点不可达。');
 }else{
  pending.push(start);seen.add(key(start));dist[key(start)]=0;
  while(pending.length){const p=pending.shift();for(const v of neighbors(p))if(!seen.has(key(v))){seen.add(key(v));parent[key(v)]=p;dist[key(v)]=dist[key(p)]+1;pending.push(v);}add(`处理 (${p})，距离 ${dist[key(p)]}。`,p);}
  if(!seen.has(key(goal)))add('搜索结束：终点不可达。');else{let p=goal;while(!eq(p,start)){path.push(p);p=parent[key(p)];}path.push(start);path.reverse();add(`最短路径 ${dist[key(goal)]} 步。`,goal,path);}
 }return frames;
}
function mount(root,id,update){
 if(!supported.includes(id))return false;
 const isGrid=['3.7','3.8'].includes(id),treeMode=['2.3','3.5'].includes(id),directed=['2.4','3.3'].includes(id);
 const panel=document.createElement('div');panel.className='search-editor demo-controls';
 panel.innerHTML=isGrid?'<label>地图预设<select data-map-preset><option value="default">默认地图</option><option value="maze">绕行与岔路</option><option value="blocked">终点不可达</option><option value="open">开放区域、多条最短路</option><option value="detour">DFS 与 BFS 路径对比</option><option value="single">单行地图</option></select></label><label>点击格子的操作<select data-edit-mode><option value="wall">切换障碍</option><option value="start">设置起点 S</option><option value="goal">设置终点 T</option></select></label><label>地图形状<select data-grid-shape><option value="3,4">小矩形 3 × 4</option><option value="6,6">正方形 6 × 6</option><option value="5,8">横向矩形 5 × 8</option><option value="8,5">纵向矩形 8 × 5</option><option value="custom">自定义尺寸</option></select></label><label>行数<input data-grid-rows type="number" min="1" max="12" value="3"></label><label>列数<input data-grid-cols type="number" min="1" max="12" value="4"></label><button type="button" data-create-grid>生成空白地图</button><div class="editor-wide"><p class="edge-help">先选择形状，再选择上方编辑操作。点击下表设置障碍、起点或终点；也可点击演示地图编辑。</p><div class="grid-editor-scroll"><table class="grid-editor-table" aria-label="可编辑地图"><tbody data-grid-editor></tbody></table></div></div>':'<label>图预设<select data-map-preset><option value="default">默认 10 节点</option><option value="tree">树形结构</option><option value="chain">单链结构</option>'+(!treeMode?'<option value="ring">环形结构</option><option value="disconnected">不连通图</option>':'')+'<option value="single">单节点</option></select></label><label>节点数（1～12）<input data-node-count type="number" min="1" max="12" value="10"></label><label>起点（字母或编号）<input data-start value="A"></label>'+(['3.3','3.6'].includes(id)?'<label>终点（字母或编号）<input data-goal value="J"></label>':'')+'<div class="editor-wide edge-editor"><div class="edge-editor-heading">连边表（'+(directed?'有向边：起点 → 终点':'无向边：两个端点')+'）</div><p class="edge-help">从图中一个节点拖到另一个节点即可连线，也可在表格里添加、修改或删除，再点击应用。</p><div class="edge-table-scroll"><table class="edge-table"><thead><tr><th>起点</th><th>终点</th><th>操作</th></tr></thead><tbody></tbody></table></div><button type="button" data-add-edge>＋ 添加一条边</button></div>' ;
 const apply=document.createElement('button');apply.type='button';apply.textContent='应用并重新演示';panel.appendChild(apply);
 const error=document.createElement('p');error.className='demo-error';error.setAttribute('role','alert');panel.appendChild(error);root.prepend(panel);
 const preset=panel.querySelector('[data-map-preset]');
 let gridRows=[];
 const gridText=()=>gridRows.map(row=>row.join('')).join('\n');
 const setGridText=text=>{gridRows=text.trim().split(/\r?\n/).map(row=>[...row.trim()]);renderEditor();};
 const renderEditor=()=>{
  const tbody=panel.querySelector('[data-grid-editor]');if(!tbody)return;tbody.replaceChildren();
  gridRows.forEach((row,r)=>{const tr=document.createElement('tr');row.forEach((x,c)=>{const td=document.createElement('td'),button=document.createElement('button');button.type='button';button.dataset.editorRow=r;button.dataset.editorCol=c;button.className='editor-cell'+(x==='#'?' wall':x==='S'?' start':x==='T'?' goal':'');button.textContent=x==='.'?'':x==='#'?'■':x;button.setAttribute('aria-label',`行 ${r}，列 ${c}，${x==='#'?'障碍':x==='S'?'起点':x==='T'?'终点':'通路'}`);td.appendChild(button);tr.appendChild(td);});tbody.appendChild(tr);});
  panel.querySelector('[data-grid-rows]').value=gridRows.length;panel.querySelector('[data-grid-cols]').value=gridRows[0].length;const shape=panel.querySelector('[data-grid-shape]'),dimensions=gridRows.length+','+gridRows[0].length;shape.value=[...shape.options].some(option=>option.value===dimensions)?dimensions:'custom';
 };
 const tbody=panel.querySelector('.edge-table tbody');
 const addRow=(a=0,b=1)=>{
  const row=document.createElement('tr');
  for(const [column,value] of [[0,a],[1,b]]){
   const cell=document.createElement('td'),select=document.createElement('select');
   const count=Math.min(12,Math.max(1,Number(panel.querySelector('[data-node-count]').value)||1));
   for(let n=0;n<Math.max(count,value+1);n++){const option=document.createElement('option');option.value=n;option.textContent=label(n);select.appendChild(option);}
   select.value=value;select.setAttribute('aria-label',column===0?'边的起点':'边的终点');cell.appendChild(select);row.appendChild(cell);
  }
  const cell=document.createElement('td'),remove=document.createElement('button');remove.type='button';remove.textContent='删除';remove.setAttribute('aria-label','删除这条边');remove.addEventListener('click',()=>row.remove());cell.appendChild(remove);row.appendChild(cell);tbody.appendChild(row);
 };
 const setEdges=edges=>{tbody.replaceChildren();edges.forEach(([a,b])=>addRow(a,b));};
 const edgeText=()=>[...tbody.rows].map(row=>[...row.querySelectorAll('select')].map(s=>s.value).join(' ')).join('\n');
 if(!isGrid)panel.querySelector('[data-add-edge]').addEventListener('click',()=>addRow(0,Number(panel.querySelector('[data-node-count]').value)>1?1:0));
 const run=()=>{try{const data=isGrid?parseGrid(gridText()):graphData(Number(panel.querySelector('[data-node-count]').value),edgeText(),panel.querySelector('[data-start]').value,panel.querySelector('[data-goal]')?.value||panel.querySelector('[data-start]').value,treeMode);const frames=isGrid?gridTrace(id,data):graphTrace(id,data);error.textContent='';update(frames);}catch(e){error.textContent=e.message;}};
 const fill=()=>{if(isGrid)setGridText(grids[preset.value]);else{let edges=graphCases[preset.value];if(preset.value==='default'&&treeMode)edges=tree;panel.querySelector('[data-node-count]').value=preset.value==='single'?1:10;panel.querySelector('[data-start]').value='A';if(panel.querySelector('[data-goal]'))panel.querySelector('[data-goal]').value=preset.value==='single'?'A':'J';setEdges(edges);}run();};
 apply.addEventListener('click',run);preset.addEventListener('change',fill);
 if(isGrid)root.addEventListener('click',event=>{
  const cell=event.target.closest('[data-grid-row],[data-editor-row]');if(!cell)return;
  try{parseGrid(gridText());const rows=gridRows.map(row=>[...row]),r=Number(cell.dataset.editorRow??cell.dataset.gridRow),c=Number(cell.dataset.editorCol??cell.dataset.gridCol),mode=panel.querySelector('[data-edit-mode]').value;if(!rows[r]||rows[r][c]===undefined)return;
   if(mode==='wall'){if('ST'.includes(rows[r][c]))return;rows[r][c]=rows[r][c]==='#'?'.':'#';}else{const symbol=mode==='start'?'S':'T';if(rows[r][c]===(symbol==='S'?'T':'S'))return;rows.forEach(row=>row.forEach((x,i)=>{if(x===symbol)row[i]='.';}));rows[r][c]=symbol;}
   setGridText(rows.map(r=>r.join('')).join('\n'));run();
  }catch(e){error.textContent=e.message;}
 });
 if(isGrid){
  panel.querySelector('[data-grid-shape]').addEventListener('change',event=>{
   if(event.target.value==='custom')return;
   const [rows,cols]=event.target.value.split(',');panel.querySelector('[data-grid-rows]').value=rows;panel.querySelector('[data-grid-cols]').value=cols;
  });
  panel.querySelector('[data-create-grid]').addEventListener('click',()=>{
   const rows=Number(panel.querySelector('[data-grid-rows]').value),cols=Number(panel.querySelector('[data-grid-cols]').value);
   if(!Number.isInteger(rows)||!Number.isInteger(cols)||rows<1||rows>12||cols<1||cols>12||rows*cols<2){error.textContent='行列数应为 1～12，至少需要两个格子。';return;}
   const data=Array.from({length:rows},()=>Array(cols).fill('.'));data[0][0]='S';data[rows-1][cols-1]='T';setGridText(data.map(row=>row.join('')).join('\n'));run();
  });
 }
 if(!isGrid){
  const view=root.querySelector('.graph-view');let dragging=null,preview=null;
  const cancel=()=>{if(preview)preview.remove();preview=null;dragging=null;view.classList.remove('link-dragging');};
  const point=event=>{const svg=view.querySelector('svg'),p=svg.createSVGPoint();p.x=event.clientX;p.y=event.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());};
  view.addEventListener('pointerdown',event=>{
   const node=event.target.closest('[data-node]');if(!node||event.button!==0)return;
   event.preventDefault();root.dispatchEvent(new Event('graph-edit-start'));dragging={node:Number(node.dataset.node),x:Number(node.getAttribute('cx')),y:Number(node.getAttribute('cy')),pointer:event.pointerId};view.setPointerCapture(event.pointerId);view.classList.add('link-dragging');
   preview=document.createElementNS('http://www.w3.org/2000/svg','line');preview.classList.add('edge-preview');preview.setAttribute('x1',dragging.x);preview.setAttribute('y1',dragging.y);preview.setAttribute('x2',dragging.x);preview.setAttribute('y2',dragging.y);view.querySelector('svg').appendChild(preview);
  });
  view.addEventListener('pointermove',event=>{if(!dragging)return;const p=point(event);preview.setAttribute('x2',p.x);preview.setAttribute('y2',p.y);});
  view.addEventListener('pointerup',event=>{
   if(!dragging)return;const from=dragging.node,toNode=document.elementFromPoint(event.clientX,event.clientY)?.closest('[data-node]');
   if(view.hasPointerCapture(event.pointerId))view.releasePointerCapture(event.pointerId);cancel();
   if(!toNode||!view.contains(toNode))return;const to=Number(toNode.dataset.node);if(from===to)return;
   const exists=[...tbody.rows].some(row=>{const [a,b]=[...row.querySelectorAll('select')].map(s=>Number(s.value));return a===from&&b===to||!directed&&a===to&&b===from;});
   if(exists){error.textContent='这两个节点已经相连，可以在表格中删除或修改。';return;}
   addRow(from,to);run();
  });
  view.addEventListener('pointercancel',cancel);view.addEventListener('lostpointercapture',cancel);
 }
 fill();return true;
}
window.SearchPlayground={mount,graphData,graphTrace,parseGrid,gridTrace,layoutGraph,supported};
})();
