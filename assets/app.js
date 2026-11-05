(()=>{
  const toggle=document.querySelector('#theme-toggle');
  function setTheme(value){document.documentElement.dataset.theme=value;toggle.querySelector('.theme-icon').textContent=value==='dark'?'☀':'☾';toggle.querySelector('.theme-label').textContent=value==='dark'?'日间模式':'夜间模式';toggle.setAttribute('aria-pressed',String(value==='dark'))}
  try{setTheme(localStorage.getItem('algorithm-notes-theme')||'light')}catch(e){setTheme('light')}
  toggle.addEventListener('click',()=>{const n=document.documentElement.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('algorithm-notes-theme',n)}catch(e){}setTheme(n)});
  document.querySelectorAll('.code-block').forEach(block=>{
    const code=block.querySelector('code'),copy=block.querySelector('[data-copy]'),notice=block.querySelector('.copy-status');
    const source=code.textContent;
    // 将文本拆成 token 后用 textContent 写入，保留复制内容并避免注入 HTML。
    const tokens=/(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|^\s*#[ \t]*\w+|\b(?:0x[\da-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)[a-zA-Z]*\b|\b[A-Za-z_]\w*\b)/gm;
    const keywords=new Set('auto bool break case char class const constexpr continue default do double else enum false float for if int long namespace nullptr private protected public return short signed sizeof static string struct switch template this throw true try typedef typename unsigned using virtual void volatile while'.split(' '));
    const types=new Set('vector unordered_map unordered_set stack queue priority_queue pair size_t string TreeNode Edge Solution'.split(' '));
    let last=0,m;const fragment=document.createDocumentFragment();
    while((m=tokens.exec(source))){
      fragment.appendChild(document.createTextNode(source.slice(last,m.index)));
      const token=m[0],span=document.createElement('span');let cls='';
      if(/^\/\//.test(token)||/^\/\*/.test(token))cls='comment';
      else if(/^['"]/.test(token))cls='string';
      else if(/^\s*#/.test(token))cls='directive';
      else if(/^\d/.test(token))cls='number';
      else if(types.has(token))cls='type';
      else if(keywords.has(token))cls='keyword';
      else if(/^\s*\(/.test(source.slice(tokens.lastIndex)))cls='function';
      span.className=cls?'syntax-'+cls:'';span.textContent=token;fragment.appendChild(span);last=tokens.lastIndex;
    }
    fragment.appendChild(document.createTextNode(source.slice(last)));code.replaceChildren(fragment);
    copy.addEventListener('click',async()=>{
      try{
        if(navigator.clipboard && window.isSecureContext)await navigator.clipboard.writeText(source);
        else {const area=document.createElement('textarea');area.value=source;area.setAttribute('readonly','');area.style.cssText='position:fixed;left:-9999px';document.body.appendChild(area);area.select();const ok=document.execCommand('copy');area.remove();if(!ok)throw Error('copy failed')}
        notice.textContent='已复制';copy.setAttribute('aria-label','已复制代码');setTimeout(()=>{notice.textContent='';copy.setAttribute('aria-label','复制代码')},2000);
      }catch(e){notice.textContent='复制失败，请手动选择代码';}
    });
  });
  const root=document.querySelector('.demo');if(!root)return;
  let frames=JSON.parse(document.getElementById('lesson-frames').textContent);
  const stage=root.querySelector('.stage'),text=root.querySelector('.step-text'),status=root.querySelector('.status'),prev=root.querySelector('[data-action=prev]'),next=root.querySelector('[data-action=next]'),graph=root.querySelector('.graph-view');
  const id=root.dataset.lesson;let i=0,timer=null,resultIndex=0;
  const configs={
    '2.3':{nodes:[['A',210,30],['B',105,105],['C',315,105],['D',55,180],['E',155,180]],edges:[[0,1],[0,2],[1,3],[1,4]],nodeCount:[1,3,5,5],edgeCount:[0,2,4,4],highlights:[[0],[0,1,2],[2,3,4],[0,1,4]]},
    '2.4':{nodes:[['A',65,165],['B',210,30],['C',355,165]],edges:[[0,1],[1,2],[2,0]],nodeCount:[3,3,3],edgeCount:[0,2,3],highlights:[[0,1,2],[0,1,2],[0,1,2]],directed:true},
    '2.5':{nodes:[['0',210,30],['1',105,95],['2',315,95],['3',40,165],['4',145,165],['5',250,165],['6',355,165],['7',250,210]],edges:[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6],[6,7],[4,7]],nodeCount:Array(9).fill(8),edgeCount:[0,1,2,3,4,5,6,7,8],highlights:[[],[0,1],[0,2],[1,3],[1,4],[2,5],[2,6],[6,7],[4,7]]},
    '2.6':{nodes:[['A',210,30],['B',85,165],['C',335,165]],edges:[[0,1],[1,2],[2,0]],nodeCount:[3,3,3,3],edgeCount:[3,3,3,3],highlights:[[],[0],[0,1],[0,1,2]]},
    '3.1':{nodes:[['A',210,30],['B',105,105],['C',315,105],['D',105,190]],edges:[[0,1],[0,2],[1,3]],nodeCount:[4,4,4,4],edgeCount:[3,3,3,3],highlights:[[0],[1],[3],[2]]},
    '3.2':{nodes:[['A',210,30],['B',105,105],['C',315,105],['D',105,190]],edges:[[0,1],[0,2],[1,3]],nodeCount:[4,4,4,4],edgeCount:[3,3,3,3],highlights:[[0],[0],[1],[3]]},
    '3.3':{nodes:[['A',210,30],['B',105,110],['C',315,110],['D',210,195]],edges:[[0,1],[0,2],[1,3],[2,3]],nodeCount:[4,4,4,4],edgeCount:[4,4,4,4],highlights:[[0],[0,1],[0,1,3],[0,2]],directed:true},
    '3.4':{nodes:[['A',210,30],['B',105,105],['C',315,105],['D',105,190]],edges:[[0,1],[0,2],[1,3]],nodeCount:[4,4,4,4],edgeCount:[3,3,3,3],highlights:[[0],[0,1,2],[1,3],[2,3]]},
    '3.5':{nodes:[['1',210,30],['2',105,105],['3',315,105],['4',55,190],['5',155,190]],edges:[[0,1],[0,2],[1,3],[1,4]],nodeCount:[5,5,5],edgeCount:[4,4,4],highlights:[[0],[1,2],[3,4]]},
    '3.6':{nodes:[['A',210,30],['B',105,110],['C',315,110],['D',210,195]],edges:[[0,1],[0,2],[1,3],[2,3]],nodeCount:[4,4,4,4],edgeCount:[4,4,4,4],highlights:[[0],[1,2],[3],[0,1,3]]}
  };
  function drawGraph(){
    const f=frames[i],d=f.diagram;
    if(f.grid){
      const wrap=document.createElement('div');wrap.className='grid-map';wrap.setAttribute('role','group');wrap.setAttribute('aria-label','网格搜索地图，点击格子可编辑');wrap.style.gridTemplateColumns=`repeat(${f.grid[0].length},1fr)`;
      const contains=(list,r,c)=>(list||[]).some(p=>p[0]===r&&p[1]===c);
      f.grid.forEach((row,r)=>[...row].forEach((value,c)=>{
        const cell=document.createElement('button'),wall=value==='#',current=f.current&&f.current[0]===r&&f.current[1]===c;
        cell.type='button';cell.dataset.gridRow=r;cell.dataset.gridCol=c;
        cell.className='map-cell'+(wall?' wall':'')+(contains(f.visited,r,c)?' visited':'')+(contains(f.frontier,r,c)?' frontier':'')+(contains(f.route,r,c)?' route':'')+(current?' current':'');
        const start=f.start||[0,0],goal=f.goal||[f.grid.length-1,row.length-1];
        const marker=r===start[0]&&c===start[1]?'S':r===goal[0]&&c===goal[1]?'T':'';
        cell.textContent=wall?'障碍':marker||String(f.distances?.[`${r},${c}`]??'');
        cell.setAttribute('aria-label',`行 ${r}，列 ${c}，${marker==='S'?'起点':marker==='T'?'终点':wall?'障碍':current?'当前位置':'可通行'}`);wrap.appendChild(cell);
      }));
      const legend=document.createElement('p');legend.className='grid-legend';legend.textContent='S 起点 · T 终点 · 蓝色已发现 · 橙色待处理 · 绿色路径 · 边框强调当前位置';graph.replaceChildren(wrap,legend);return;
    }
    const c=d?{...d,nodeCount:Array(frames.length).fill(d.nodes.length),edgeCount:Array(frames.length).fill(d.edges.length),highlights:frames.map(x=>x.highlight||[])}:configs[id];if(!c)return;
    const routes=f.routes||[];if(resultIndex>=routes.length)resultIndex=0;
    const route=routes[resultIndex]||f.route||[],routeNodes=new Set(route);
    const isRouteEdge=(a,b)=>route.some((v,index)=>index>0&&(route[index-1]===a&&v===b||!c.directed&&route[index-1]===b&&v===a));
    const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox',c.viewBox?c.viewBox.join(' '):'-12 -12 444 276');svg.setAttribute('role','group');svg.setAttribute('aria-label','图中节点与连接关系，可从一个节点拖动到另一个节点添加连边');svg.classList.add('graph-diagram');
    if(c.directed){const defs=document.createElementNS(ns,'defs'),marker=document.createElementNS(ns,'marker'),arrow=document.createElementNS(ns,'path');marker.setAttribute('id','graph-arrow');marker.setAttribute('viewBox','0 0 10 10');marker.setAttribute('refX','8');marker.setAttribute('refY','5');marker.setAttribute('markerWidth','6');marker.setAttribute('markerHeight','6');marker.setAttribute('orient','auto-start-reverse');arrow.setAttribute('d','M 0 0 L 10 5 L 0 10 z');arrow.setAttribute('fill','var(--muted)');marker.appendChild(arrow);defs.appendChild(marker);const routeMarker=marker.cloneNode(true);routeMarker.setAttribute('id','graph-arrow-route');routeMarker.querySelector('path').setAttribute('fill','var(--route-stroke)');defs.appendChild(routeMarker);svg.appendChild(defs)}
    c.edges.slice(0,c.edgeCount[i]).forEach(([a,b],edgeIndex)=>{const p=c.nodes[a],q=c.nodes[b],dx=q[1]-p[1],dy=q[2]-p[2],d=Math.hypot(dx,dy),line=document.createElementNS(ns,'line');line.setAttribute('x1',p[1]+dx/d*20);line.setAttribute('y1',p[2]+dy/d*20);line.setAttribute('x2',q[1]-dx/d*(c.directed?25:20));line.setAttribute('y2',q[2]-dy/d*(c.directed?25:20));line.classList.add('graph-edge');if(id==='2.5' && edgeIndex===i-1)line.classList.add('graph-edge-new');line.setAttribute('stroke','var(--muted)');line.setAttribute('stroke-width','2');if(c.directed)line.setAttribute('marker-end','url(#graph-arrow)');if(isRouteEdge(a,b)){line.classList.add('result-edge');line.setAttribute('stroke','var(--route-stroke)');line.setAttribute('stroke-width','4');if(c.directed)line.setAttribute('marker-end','url(#graph-arrow-route)');}svg.appendChild(line)});
    c.nodes.slice(0,c.nodeCount[i]).forEach(([label,x,y],j)=>{const circle=document.createElementNS(ns,'circle');circle.classList.add('graph-node');circle.dataset.node=String(j);circle.setAttribute('aria-label','节点 '+label);if(c.highlights[i].includes(j))circle.classList.add('graph-node-active');if(routeNodes.has(j))circle.classList.add('result-node');circle.setAttribute('cx',x);circle.setAttribute('cy',y);circle.setAttribute('r','20');circle.setAttribute('fill',c.highlights[i].includes(j)?'var(--active)':'var(--paper)');circle.setAttribute('stroke','var(--accent)');circle.setAttribute('stroke-width','2');svg.appendChild(circle);const t=document.createElementNS(ns,'text');t.setAttribute('x',x);t.setAttribute('y',y);t.style.pointerEvents='none';t.setAttribute('text-anchor','middle');t.setAttribute('dominant-baseline','central');t.setAttribute('fill','var(--ink)');t.textContent=label;svg.appendChild(t)});graph.replaceChildren(svg);
    if(route.length){const info=document.createElement('p');info.className='result-route-label';info.textContent='高亮路径：'+route.map(n=>c.nodes[n][0]).join(' → ');graph.appendChild(info);}
    if(routes.length>1){const label=document.createElement('label');label.className='result-route-select';label.textContent='切换结果路径 ';const select=document.createElement('select');select.setAttribute('aria-label','切换结果路径');routes.forEach((path,index)=>{const option=document.createElement('option');option.value=index;option.textContent=`第 ${index+1} 条：`+path.map(n=>c.nodes[n][0]).join(' → ');select.appendChild(option);});select.value=resultIndex;select.addEventListener('change',()=>{resultIndex=Number(select.value);drawGraph();});label.appendChild(select);graph.appendChild(label);}
  }
  function draw(){
    const f=frames[i];
    if(f.indexed){
      const compatible=stage.children.length===f.cells.length && [...stage.children].every(el=>el.classList.contains('array-cell'));
      if(!compatible){
        const cells=f.cells.map((_,j)=>{const el=document.createElement('span');el.className='cell array-cell';const pointer=document.createElement('span');pointer.className='pointer-label';const number=document.createElement('span');number.className='cell-value';const index=document.createElement('span');index.className='cell-index';index.textContent='下标 '+j;el.appendChild(pointer);el.appendChild(number);el.appendChild(index);return el});
        if(!cells.length){const empty=document.createElement('span');empty.className='empty-array';empty.textContent='空数组：没有元素';cells.push(empty)}stage.replaceChildren(...cells);
      }
      f.cells.forEach((value,j)=>{
        const el=stage.children[j],number=el.querySelector('.cell-value'),pointer=el.querySelector('.pointer-label');
        const changed=number.textContent!==''&&number.textContent!==value;
        number.textContent=value;
        const names=Object.entries(f.pointers||{}).filter(([,position])=>position===j).map(([name])=>name);
        pointer.textContent=names.join(' · ')||' ';
        const inRange=f.range&&j>=f.range[0]&&j<=f.range[1];
        el.className='cell array-cell'+(inRange?' in-range':'')+(f.range&&!inRange?' outside-range':'')+((f.active||[]).includes(j)?' active':'');
        if(changed){void el.offsetWidth;el.classList.add('cell-write')}
        el.setAttribute('aria-label','下标 '+j+'，值 '+value+(names.length?'，指针 '+names.join('、'):''));
      });
      const outside=Object.entries(f.pointers||{}).filter(([,position])=>position<0||position>=f.cells.length).map(([name,position])=>name+' = '+position+'（数组范围外）');
      root.querySelector('.pointer-outside').textContent=outside.join('；');
    }else{
      const cells=f.cells.map((value,j)=>{const el=document.createElement('span');el.className='cell'+((f.active||[]).includes(j)?' active':'');el.textContent=value;return el});
      stage.replaceChildren(...cells);root.querySelector('.pointer-outside').textContent='';
    }
    drawGraph();text.textContent=f.text;status.textContent=`第 ${i+1} / ${frames.length} 步`;prev.disabled=i===0;next.disabled=i===frames.length-1;
  }
  const play=root.querySelector('[data-action=play]');
  function stop(){if(timer!==null){clearInterval(timer);timer=null}if(play)play.textContent='自动播放';}
  root.addEventListener('graph-edit-start',stop);
  prev.addEventListener('click',()=>{stop();if(i>0){i--;draw()}});
  next.addEventListener('click',()=>{stop();if(i<frames.length-1){i++;draw()}});
  root.querySelector('[data-action=reset]').addEventListener('click',()=>{stop();i=0;draw()});
  if(play)play.addEventListener('click',()=>{if(timer!==null){stop();return}if(i===frames.length-1)i=0;draw();play.textContent='暂停播放';timer=setInterval(()=>{if(i>=frames.length-1){stop();return}i++;draw();if(i>=frames.length-1)stop()},900)});
  if(window.SearchPlayground?.supported.includes(id)){
    window.SearchPlayground.mount(root,id,newFrames=>{stop();frames=newFrames;i=0;draw()});
  }else if(root.querySelector('[data-input=array]')){
    const api=window.AlgorithmTraces,defaults=api.defaults[id],array=root.querySelector('[data-input=array]'),target=root.querySelector('[data-input=target]'),preset=root.querySelector('[data-input=preset]'),message=root.querySelector('.demo-error');
    const cases={
      '1.1':{first:{nums:[1,3,5],value:1},last:{nums:[1,3,5],value:5},single:{nums:[4],value:4},empty:{nums:[],value:3},missing:{nums:[-4,0,2,7,10],value:3}},
      '1.2':{first:{nums:[1,3,5,6],value:0},last:{nums:[1,3,5,6],value:9},single:{nums:[4],value:4},empty:{nums:[],value:5},missing:{nums:[1,3,5,6],value:7}},
      '1.3':{first:{nums:[1,2,4,6],value:3},last:{nums:[1,2,4,6],value:10},single:{nums:[2],value:4},empty:{nums:[],value:9},missing:{nums:[1,2,4,8,12],value:30}},
      '1.4':{first:{nums:[1,1,2,3],value:null},last:{nums:[1,2,3,3],value:null},single:{nums:[4],value:null},empty:{nums:[],value:null},missing:{nums:[1,1,1,2,2,3],value:null}},
      '1.5':{first:{nums:[3,2,2],value:3},last:{nums:[2,2,3],value:3},single:{nums:[3],value:3},empty:{nums:[],value:3},missing:{nums:[1,2,3,4],value:9}},
      '1.6':{first:{nums:[7,1,1],value:7},last:{nums:[1,1,7],value:7},single:{nums:[7],value:7},empty:{nums:[],value:7},missing:{nums:[1,1,1],value:10}},
      '1.7':{first:{nums:[...'abcdefghi']},last:{nums:[...'aaaaaaaaa']},single:{nums:['a']},empty:{nums:[]},missing:{nums:[...'abba']}},
      '1.8':{first:{nums:[1,2,3,4,5,6,7,8,9]},last:{nums:[9,8,7,6,5,4,3,2,1]},single:{nums:[4]},empty:{nums:[]},missing:{nums:[3,1,3,2,1,2,3,1,2]}}
    };
    function fill(choice){const data=choice==='default'?defaults:cases[id][choice];array.value=data.nums.join(id==='1.7'?'':', ');if(target)target.value=String(data.value);}
    function apply(){stop();try{const data=api.parse(id,array.value,target?target.value:'');frames=api.trace(id,data.arr,data.value);i=0;message.textContent='';draw()}catch(err){message.textContent=err.message;}}
    preset.addEventListener('change',()=>{fill(preset.value);apply()});root.querySelector('[data-action=apply]').addEventListener('click',apply);
    fill('default');apply();
  }else draw();
})();
