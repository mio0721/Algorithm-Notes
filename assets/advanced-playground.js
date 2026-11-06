/* Advanced lesson traces are generated from the downloadable Python implementation. */
(() => {
  'use strict';
  const ns = 'http://www.w3.org/2000/svg';
  const element = (name, attrs = {}, text) => {
    const node = document.createElementNS(ns, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const svgRoot = (height, label) => element('svg', {
    viewBox: `0 0 600 ${height}`, class: 'advanced-diagram', role: 'img', 'aria-label': label
  });
  const line = (svg, x1, y1, x2, y2, color = 'var(--muted)', width = 2) => {
    svg.append(element('line', {x1, y1, x2, y2, stroke: color, 'stroke-width': width}));
  };
  const text = (svg, x, y, value, attrs = {}) => {
    svg.append(element('text', {x, y, fill: 'var(--ink)', 'font-size': 15, ...attrs}, value));
  };

  function network(f) {
    const d = f.network, svg = svgRoot(390, '图的连接、边权及算法当前状态');
    const nodes = d.nodes.map(([label,x,y]) => [label,x*1.2+10,y+10]);
    if (d.directed) {
      const defs=element('defs'),marker=element('marker',{id:'advanced-arrow',viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:6,markerHeight:6,orient:'auto'});
      marker.append(element('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:'var(--muted)'}));
      defs.append(marker);svg.append(defs);
    }
    const selected = (a,b) => (f.chosenEdges||[]).some(([u,v]) => u===a&&v===b||!d.directed&&u===b&&v===a)
      || (f.route||[]).some((v,i,r)=>i>0&&(r[i-1]===a&&v===b||!d.directed&&r[i-1]===b&&v===a));
    const edgeLabels=[];
    d.edges.forEach(([a,b,weight]) => {
      const [,x1,y1]=nodes[a],[,x2,y2]=nodes[b],length=Math.hypot(x2-x1,y2-y1)||1;
      const edge=element('line',{x1:x1+(x2-x1)*22/length,y1:y1+(y2-y1)*22/length,
        x2:x2-(x2-x1)*26/length,y2:y2-(y2-y1)*26/length,
        stroke:selected(a,b)?'var(--route-stroke)':'var(--muted)','stroke-width':selected(a,b)?4:2});
      if(d.directed)edge.setAttribute('marker-end','url(#advanced-arrow)');
      svg.append(edge);
      if(weight!==undefined){
        const x=(x1+x2)/2,y=(y1+y2)/2;
        edgeLabels.push([x,y,weight]);
      }
    });
    // Draw every edge before every label, so later edges never paint over text.
    edgeLabels.forEach(([x,y,weight])=>{
      const width=Math.max(28,String(weight).length*10+12);
      svg.append(element('rect',{x:x-width/2,y:y-11,width,height:22,rx:4,fill:'var(--paper)'}));
      text(svg,x,y+5,weight,{'text-anchor':'middle'});
    });
    nodes.forEach(([label,x,y],i)=>{
      svg.append(element('circle',{cx:x,cy:y,r:21,fill:(f.highlight||[]).includes(i)?'var(--active)':'var(--paper)',stroke:'var(--accent)','stroke-width':2}));
      text(svg,x,y+5,label,{'text-anchor':'middle','font-weight':700});
      const values=f.nodeNotes?.[i]||[f.distances?.[i]!==undefined&&f.distances[i]!==-1?'d='+f.distances[i]:null,f.parents?.[i]>=0?'来自 '+nodes[f.parents[i]][0]:null,(f.settled||[]).includes(i)?'已确定':null].filter(Boolean);
      values.forEach((value,j)=>text(svg,x,y+36+j*17,value,{'text-anchor':'middle','font-size':13,fill:'var(--muted)',class:'node-record'}));
      if(f.warning&&(f.highlight||[]).includes(i))svg.append(element('circle',{cx:x,cy:y,r:26,fill:'none',stroke:'#ee9b43','stroke-width':3,class:'error-location'}));
    });
    return svg;
  }

  function matrix(f) {
    const wrap=document.createElement('div');wrap.className='matrix-scroll';
    const table=document.createElement('table');table.className='dp-matrix';
    const header=document.createElement('tr');header.append(document.createElement('th'));
    const columns=f.matrix.reduce((n,row)=>Math.max(n,row.length),0);
    for(let c=0;c<columns;c++){const th=document.createElement('th');th.textContent=f.colLabels?.[c]??c;header.append(th);}
    table.append(header);
    f.matrix.forEach((row,r)=>{
      const tr=document.createElement('tr'),th=document.createElement('th');th.textContent=f.rowLabels?.[r]??r;tr.append(th);
      row.forEach((value,c)=>{const td=document.createElement('td');td.textContent=value;
        if(f.matrixActive?.[0]===r&&(f.mistakeTimeline||f.matrixActive?.[1]===c))td.className='active';tr.append(td);});
      table.append(tr);
    });
    wrap.append(table);return wrap;
  }

  function scene(f) {
    const d=f.scene,svg=svgRoot(520,'连续空间采样树；绿色为当前结果路径');
    const x=v=>55+v*45,y=v=>465-v*43;
    for(let v=0;v<=10;v++){
      line(svg,x(v),y(0),x(v),y(10),'var(--line)',1);
      line(svg,x(0),y(v),x(10),y(v),'var(--line)',1);
      text(svg,x(v),y(0)+22,v,{'text-anchor':'middle','font-size':12});
      text(svg,x(0)-15,y(v)+4,v,{'text-anchor':'end','font-size':12});
    }
    d.obstacles.forEach(([left,bottom,right,top])=>svg.append(element('rect',{
      x:x(left),y:y(top),width:(right-left)*45,height:(top-bottom)*43,fill:'var(--muted)',opacity:0.65
    })));
    d.points.forEach((p,i)=>{if(d.parents[i]>=0){const q=d.points[d.parents[i]];line(svg,x(p[0]),y(p[1]),x(q[0]),y(q[1]),'var(--accent)',1.3);}});
    if(d.route?.length)svg.append(element('polyline',{points:d.route.map(p=>`${x(p[0])},${y(p[1])}`).join(' '),fill:'none',stroke:'var(--route-stroke)','stroke-width':4}));
    d.points.forEach(p=>svg.append(element('circle',{cx:x(p[0]),cy:y(p[1]),r:2,fill:'var(--accent)'})));
    for(const [p,label] of [[d.start,'S'],[d.goal,'T']]){
      svg.append(element('circle',{cx:x(p[0]),cy:y(p[1]),r:9,fill:'var(--paper)',stroke:'var(--route-stroke)','stroke-width':2}));
      text(svg,x(p[0])+12,y(p[1])-8,label);
    }
    if(d.sample){const p=d.sample;text(svg,x(p[0]),y(p[1]),'+',{fill:'var(--ink)','font-size':24});}
    text(svg,60,510,'横纵坐标：空间单位；+ 当前采样；绿色：已验证可行路径');
    return svg;
  }

  function chart(f) {
    const wrap=document.createElement('div');wrap.className='trajectory-charts';
    ['位置 s / m','速度 v / (m/s)','加速度 a / (m/s²)'].forEach((label,j)=>{
      const svg=svgRoot(210,label),samples=f.chart.all,column=j+1;
      const values=samples.map(row=>row[column]);
      let low=Math.min(0,...values),high=Math.max(0,...values);
      if(high-low<1e-9){low-=1;high+=1;}
      const x=t=>65+t/samples.at(-1)[0]*490,y=v=>165-(v-low)/(high-low)*115;
      text(svg,65,25,label);line(svg,65,50,65,165);line(svg,65,y(0),555,y(0));
      text(svg,10,55,high.toFixed(2));text(svg,10,170,low.toFixed(2));
      text(svg,65,198,'0');text(svg,500,198,`${samples.at(-1)[0]} s`);
      svg.append(element('polyline',{points:samples.map(row=>`${x(row[0])},${y(row[column])}`).join(' '),fill:'none',stroke:'var(--muted)','stroke-width':1.5}));
      svg.append(element('polyline',{points:samples.slice(0,f.chart.current+1).map(row=>`${x(row[0])},${y(row[column])}`).join(' '),fill:'none',stroke:'var(--accent)','stroke-width':3}));
      const current=samples[f.chart.current];svg.append(element('circle',{cx:x(current[0]),cy:y(current[column]),r:5,fill:'var(--route-stroke)'}));wrap.append(svg);
    });return wrap;
  }

  function intervals(f) {
    const d=f.intervals,svg=svgRoot(Math.max(170,d.all.length*35+55),'任务区间：绿色为已选择任务');
    const lo=Math.min(0,...d.all.map(p=>p[0])),hi=Math.max(1,...d.all.map(p=>p[1]));
    d.all.forEach(([a,b],i)=>{
      const chosen=d.chosen.some(p=>p[0]===a&&p[1]===b);
      const x=v=>100+(v-lo)/(hi-lo)*440,y=35+i*35;
      text(svg,5,y+5,`[${a},${b})`);
      if(f.intervalValues)text(svg,390,y-10,(f.intervalValues[i])+(f.intervalValues[2]===10?' 收益':' 时长'),{'font-size':11});
      line(svg,x(a),y,x(b),y,chosen?'var(--route-stroke)':'var(--muted)',i===d.current?9:5);
      text(svg,x(a),y-8,a,{'font-size':11});text(svg,x(b),y-8,b,{'font-size':11});
    });return svg;
  }

  function structures(f){
    const wrap=document.createElement('div');wrap.className='structure-groups';
    f.containers.forEach(group=>{const section=document.createElement('section'),title=document.createElement('strong'),items=document.createElement('div');title.textContent=group.name;items.className='structure-items';
      (group.values.length?group.values:['∅ 空']).forEach(value=>{const box=document.createElement('span');box.className='structure-item';box.textContent=value;items.append(box);});section.append(title,items);wrap.append(section);});return wrap;
  }
  function measurements(f){
    const svg=svgRoot(290,'操作计数或测量值');
    if(f.work){const {rows,cols,done}=f.work;for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){
      const x=90+c*100,y=35+r*52;svg.append(element('rect',{x,y,width:84,height:38,rx:5,fill:r*cols+c<done?'var(--active)':'var(--paper)',stroke:'var(--accent)'}));text(svg,x+42,y+24,`${r},${c}`,{'text-anchor':'middle'});
    }text(svg,90,275,`外层 ${rows} 次 × 内层 ${cols} 次；已执行 ${done} 次`);}
    if(f.bars){const max=Math.max(...f.bars.map(x=>x[1]));f.bars.forEach(([name,value],i)=>{const y=45+i*85;text(svg,15,y,name);svg.append(element('rect',{x:155,y:y-20,width:value/max*390,height:30,rx:4,fill:'var(--active)',stroke:'var(--accent)'}));text(svg,155,y+35,`${value} ${f.barUnit||''}`);});}return svg;
  }
  function plot(f){
    const d=f.plot,svg=svgRoot(300,'带单位的函数曲线与检查位置'),xs=d.points.map(p=>p[0]),ys=d.points.map(p=>p[1]);
    const maxX=Math.max(...xs)||1,maxY=Math.max(...ys,d.limit||0)*1.2||1,x=v=>65+v/maxX*470,y=v=>235-v/maxY*180;
    line(svg,65,45,65,235);line(svg,65,235,550,235);text(svg,460,280,d.xLabel);text(svg,15,25,d.yLabel);
    svg.append(element('polyline',{points:d.points.map(([a,b])=>`${x(a)},${y(b)}`).join(' '),fill:'none',stroke:'var(--accent)','stroke-width':3}));
    if(d.limit!==null){line(svg,65,y(d.limit),550,y(d.limit),'#ee9b43');text(svg,400,y(d.limit)-8,'上限 '+d.limit);}
    d.marked.forEach(i=>{const [a,b]=d.points[i];svg.append(element('circle',{cx:x(a),cy:y(b),r:6,fill:'#ee9b43'}));text(svg,x(a),y(b)-12,`(${a}, ${b})`,{'text-anchor':'middle','font-size':12});});return svg;
  }
  function robot(f){
    const svg=svgRoot(330,'机器人尺寸与障碍膨胀示意'),d=f.robot;
    if(d.kind==='corridor'){
      svg.append(element('rect',{x:70,y:20,width:450,height:85,fill:'var(--muted)'}),element('rect',{x:70,y:225,width:450,height:85,fill:'var(--muted)'}));
      line(svg,80,165,510,165,'var(--accent)',2);text(svg,85,145,'走廊净宽 0.8m');
      svg.append(element('circle',{cx:330,cy:165,r:d.phase===1?4:75,fill:'var(--active)',stroke:d.phase>=2?'#ee9b43':'var(--accent)','stroke-width':3,opacity:.8}));
      text(svg,280,170,d.phase===1?'点模型':'直径 1m');if(d.phase===3)text(svg,90,325,'膨胀半径 0.5m 后：无可行中心通道');
    }else{
      for(let r=0;r<7;r++)for(let c=0;c<9;c++){const obstacle=r===3&&c===4,expanded=d.phase===3&&Math.hypot(r-3,c-4)<=3;
        svg.append(element('rect',{x:80+c*40,y:15+r*40,width:38,height:38,fill:obstacle?'var(--muted)':expanded?'var(--active)':'var(--paper)',stroke:'var(--line)'}));}
      text(svg,80,320,'1 格 = 0.1m；0.3m 半径 = 3 格；绿色为膨胀区域');
    }return svg;
  }
  function draw(container,f) {
    const parts=[];
    if(f.network && f.distances && f.parents){
      const layout=document.createElement('div');layout.className='network-state-layout';
      const drawing=document.createElement('div');drawing.className='network-state-graph';drawing.append(network(f));
      const panel=document.createElement('section');panel.className='network-state-panel';
      const title=document.createElement('strong');title.textContent='最短距离表';panel.append(title);
      const caption=document.createElement('p');caption.textContent='随每次出队和松弛更新；∞ 表示尚未找到路径。';panel.append(caption);
      const table=document.createElement('table');table.className='network-state-table';
      const head=document.createElement('thead'),header=document.createElement('tr');
      ['节点','当前距离','前驱','状态'].forEach(value=>{const th=document.createElement('th');th.scope='col';th.textContent=value;header.append(th);});head.append(header);table.append(head);
      const body=document.createElement('tbody');
      f.network.nodes.forEach(([name],i)=>{const tr=document.createElement('tr');if(f.updated===i)tr.classList.add('state-updated');if((f.highlight||[]).includes(i))tr.classList.add('state-current');
        const previous=f.parents[i];const values=[name,String(f.distances[i]),previous<0?'—':f.network.nodes[previous][0],(f.settled||[]).includes(i)?'已确定':f.distances[i]==='∞'?'未发现':'待处理'];
        values.forEach((value,j)=>{const cell=document.createElement(j?'td':'th');if(!j)cell.scope='row';cell.textContent=value;tr.append(cell);});body.append(tr);});
      table.append(body);panel.append(table);layout.append(drawing,panel);parts.push(layout);
    } else if(f.network)parts.push(network(f));
    if(f.scene)parts.push(scene(f));
    if(f.chart)parts.push(chart(f));
    if(f.intervals)parts.push(intervals(f));
    if(f.containers)parts.push(structures(f));
    if(f.work||f.bars)parts.push(measurements(f));
    if(f.plot)parts.push(plot(f));
    if(f.robot)parts.push(robot(f));
    if(f.matrix)parts.push(matrix(f));
    if(!parts.length){
      if(container.closest('.advanced-demo'))container.replaceChildren();
      return false;
    }
    container.replaceChildren(...parts);return true;
  }

  // Live map editing uses the same four-neighbor A* definition as the Python demo.
  function astar(grid,start,goal,useHeuristic) {
    const key=p=>p.join(','),h=p=>useHeuristic?Math.abs(p[0]-goal[0])+Math.abs(p[1]-goal[1]):0;
    const pending=[{p:start,g:0,f:h(start)}],distance=new Map([[key(start),0]]),parent=new Map(),visited=[],frames=[];
    const scores=()=>Object.fromEntries(grid.flatMap((row,r)=>[...row].flatMap((value,c)=>{
      if(value==='#')return [];
      const g=distance.get(`${r},${c}`)??Infinity,estimate=h([r,c]);
      return [[`${r},${c}`,{w:1,g,h:estimate,f:g+estimate}]];
    })));
    while(pending.length){
      pending.sort((a,b)=>a.f-b.f||a.g-b.g||a.p[0]-b.p[0]||a.p[1]-b.p[1]);
      const {p:u,g}=pending.shift();if(distance.get(key(u))!==g)continue;visited.push(u);
      frames.push({text:`扩展 (${u})：g=${g}，h=${h(u)}，f=${g+h(u)}`,cells:[],active:[],grid,start,goal,current:u,visited:[...visited],frontier:pending.map(x=>x.p),scores:scores(),parents:Object.fromEntries([...parent].map(([k,p])=>[k,p.join(',')])),scoreKind:'astar'});
      if(key(u)===key(goal)){
        const route=[u];let p=u;while(key(p)!==key(start)){p=parent.get(key(p));route.push(p);}route.reverse();
        frames.push({text:`最短路径 ${route.length-1} 步；扩展 ${visited.length} 个格子。`,cells:[],active:[],grid,start,goal,visited,route,scores:scores(),parents:Object.fromEntries([...parent].map(([k,p])=>[k,p.join(',')])),scoreKind:'astar'});return frames;
      }
      for(const [dr,dc] of [[1,0],[-1,0],[0,1],[0,-1]]){
        const v=[u[0]+dr,u[1]+dc];if(v[0]<0||v[0]>=grid.length||v[1]<0||v[1]>=grid[0].length||grid[v[0]][v[1]]==='#')continue;
        if(g+1<(distance.get(key(v))??Infinity)){distance.set(key(v),g+1);parent.set(key(v),u);pending.push({p:v,g:g+1,f:g+1+h(v)});}
      }
    }
    frames.push({text:'终点不可达。',cells:[],active:[],grid,start,goal,visited,route:[],scores:scores(),scoreKind:'astar'});return frames;
  }

  function mount(root,id,update) {
    root.classList.add('advanced-demo');
    const presets=JSON.parse(document.getElementById('lesson-presets').textContent);
    const controls=document.createElement('div');controls.className='demo-controls advanced-controls';
    const label=document.createElement('label');label.textContent='场景预设';
    const select=document.createElement('select');select.setAttribute('aria-label','演示场景');
    presets.forEach((item,i)=>{const option=document.createElement('option');option.value=i;option.textContent=item.name;select.append(option);});
    label.append(select);controls.append(label);
    const info=document.createElement('p');info.className='muted';info.textContent='正常场景由算法计算，错误场景逐步复现具体反例；可执行、回退或自动播放。';controls.append(info);
    root.prepend(controls);
    let editing=false,map,start,goal;
    const fixedInfo=document.createElement('p');fixedInfo.className='fixed-scene-input';fixedInfo.hidden=true;controls.append(fixedInfo);
    root.addEventListener('mistake-editor',event=>{
      const {active,frame:f}=event.detail;
      [...controls.children].filter(el=>el.querySelector('select')&&!el.contains(select)||el.tagName==='BUTTON').forEach(el=>el.hidden=active&&!f?.grid);
      fixedInfo.hidden=!active||Boolean(f?.grid);
      if(!active)return;
      fixedInfo.textContent=f.network?'固定图：节点 '+f.network.nodes.map(n=>n[0]).join('、')+'；边 '+f.network.edges.map(([a,b,w])=>f.network.nodes[a][0]+'→'+f.network.nodes[b][0]+(w===undefined?'':'（'+w+'）')).join('，'):f.robot?'固定机器人尺寸与障碍示意：以图中的物理尺寸及分辨率为准，不能编辑。':'固定示例：按下方图形与操作逐步演示。';
      const shape=controls.querySelector('select[aria-label="地图形状"]');
      if(shape&&f.grid){const value=f.grid.length+','+f.grid[0].length;if(![...shape.options].some(o=>o.value===value)){const o=document.createElement('option');o.value=value;o.textContent=f.grid.length+' 行 × '+f.grid[0].length+' 列（固定例子）';shape.append(o);}shape.value=value;}
      if(shape&&!f.grid){shape.value='';}
    });
    const load=()=>{editing=false;const frames=presets[Number(select.value)].frames;
      if(id==='5.3'||id==='6.1'){map=frames[0].grid.map(row=>row.split(''));start=[...frames[0].start];goal=[...frames[0].goal];}
      update(frames);
    };
    select.addEventListener('change',load);
    if(id==='5.3'||id==='6.1'){
      const modeLabel=document.createElement('label');modeLabel.textContent='点击格子设置';
      const mode=document.createElement('select');[['wall','切换障碍'],['start','起点 S'],['goal','终点 T']].forEach(([value,title])=>{const option=document.createElement('option');option.value=value;option.textContent=title;mode.append(option);});modeLabel.append(mode);controls.append(modeLabel);
      const shapeLabel=document.createElement('label');shapeLabel.textContent='地图形状';const shape=document.createElement('select');shape.setAttribute('aria-label','地图形状');
      [[6,9],[8,8],[4,12],[10,10]].forEach(([r,c])=>{const option=document.createElement('option');option.value=`${r},${c}`;option.textContent=`${r} 行 × ${c} 列`;shape.append(option);});shapeLabel.append(shape);controls.append(shapeLabel);
      const algorithm=document.createElement('select');algorithm.setAttribute('aria-label','搜索算法');
      [['astar','A*：曼哈顿启发式'],['uniform','Dijkstra：h=0']].forEach(([value,title])=>{const o=document.createElement('option');o.value=value;o.textContent=title;algorithm.append(o);});const al=document.createElement('label');al.textContent='搜索方法';al.append(algorithm);controls.append(al);
      const preview=()=>update([{text:'编辑地图后点击“计算路径”；S/T 始终可通行。',cells:[],active:[],grid:map.map(row=>row.join('')),start,goal}]);
      shape.addEventListener('change',()=>{const [r,c]=shape.value.split(',').map(Number);map=Array.from({length:r},()=>Array(c).fill('.'));start=[0,0];goal=[r-1,c-1];editing=true;preview();});
      const run=document.createElement('button');run.type='button';run.textContent='计算路径';run.addEventListener('click',()=>update(astar(map.map(row=>row.join('')),start,goal,algorithm.value==='astar')));controls.append(run);
      root.addEventListener('click',event=>{
        if(root.classList.contains('mistake-active'))return;
        const cell=event.target.closest('[data-grid-row]');if(!cell)return;
        const p=[Number(cell.dataset.gridRow),Number(cell.dataset.gridCol)],same=q=>p[0]===q[0]&&p[1]===q[1];
        if(mode.value==='start'){if(same(goal))return;start=p;map[p[0]][p[1]]='.';}
        else if(mode.value==='goal'){if(same(start))return;goal=p;map[p[0]][p[1]]='.';}
        else if(!same(start)&&!same(goal))map[p[0]][p[1]]=map[p[0]][p[1]]==='#'?'.':'#';
        editing=true;preview();
      });
    }
    load();
  }
  window.AdvancedPlayground={draw,mount,astar};
})();
