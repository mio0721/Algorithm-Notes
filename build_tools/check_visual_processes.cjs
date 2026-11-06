// Uses Chrome's native DevTools protocol; no npm dependency is required.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..');
let seq=0;const pending=new Map(),errors=[];
async function main(){
 const tabs=await(await fetch('http://127.0.0.1:9337/json')).json();
 const ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
 await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);if(m.error)p.reject(Error(JSON.stringify(m.error)));else p.resolve(m.result);}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text+' '+JSON.stringify(m.params.exceptionDetails.exception));};
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 await call('Runtime.enable');await call('Page.enable');
 await call('Emulation.setDeviceMetricsOverride',{width:1280,height:1000,deviceScaleFactor:1,mobile:false});
 const files=fs.readdirSync(path.join(root,'lessons'),{recursive:true}).filter(f=>f.endsWith('.html'));
 let count=0,frames=0;
 for(const file of files){
  const url=pathToFileURL(path.join(root,'lessons',file)).href;
  await call('Page.navigate',{url});
  await evaluate(`new Promise((resolve,reject)=>{let n=0;const check=()=>{if(document.readyState==='complete'&&document.querySelector('.demo select option[value="__mistake__1"]'))resolve(true);else if(n++>100)reject(Error('page not ready'));else setTimeout(check,30)};check()})`);
  for(let c=1;c<=2;c++){
   const result=await evaluate(`(()=>{const root=document.querySelector('.demo'),select=[...root.querySelectorAll('select')].find(s=>[...s.options].some(o=>o.value==='__mistake__1'));select.value='__mistake__${c}';select.dispatchEvent(new Event('change',{bubbles:true}));let warning=false,n=0;const texts=[];do{warning ||= !!root.querySelector('.mistake-alert');texts.push(root.querySelector('.step-text').textContent);if(root.querySelector('[data-action=next]').disabled)break;root.querySelector('[data-action=next]').click();}while(++n<600);return {warning,n:n+1,graphic:!!root.querySelector('.graph-view svg,.graph-view .grid-map,.graph-view .structure-groups,.stage .array-cell,.stage .empty-array,.graph-view table,.graph-view .recursion-demo'),locked:[...root.querySelectorAll('input')].every(e=>e.disabled),selectorEnabled:!select.disabled,hiddenTable:!!root.querySelector('.mistakeTimeline'),text:texts.at(-1)}})()`);
   if(!result.warning||!result.graphic||!result.locked||!result.selectorEnabled)throw Error(file+' case '+c+' '+JSON.stringify(result));
   const sync=await evaluate(`(()=>{const r=document.querySelector('.demo'),s=[...r.querySelectorAll('select')].find(s=>[...s.options].some(o=>o.value==='__mistake__1'));s.dispatchEvent(new Event('change',{bubbles:true}));const f=JSON.parse(document.getElementById('mistake-frames').textContent)[${c-1}].frames[0];const n=r.querySelector('[data-node-count]');if(n&&f.network&&Number(n.value)!==f.network.nodes.length)throw Error('node count mismatch');const edges=r.querySelector('.edge-table tbody');if(edges&&f.network&&edges.rows.length!==f.network.edges.length)throw Error('edge input mismatch');const row=r.querySelector('[data-grid-rows]');if(row&&f.grid&&Number(row.value)!==f.grid.length)throw Error('grid rows mismatch');const cell=r.querySelector('[data-grid-row]');if(cell){const before=r.querySelector('.step-text').textContent;cell.dispatchEvent(new MouseEvent('click',{bubbles:true}));if(before!==r.querySelector('.step-text').textContent)throw Error('locked map was modified');}return true;})()`);
   count++;frames+=result.n;
  }
  await evaluate(`(()=>{const r=document.querySelector('.demo'),s=[...r.querySelectorAll('select')].find(s=>[...s.options].some(o=>o.value==='__mistake__1'));s.value=s.options[0].value;s.dispatchEvent(new Event('change',{bubbles:true}));if([...r.querySelectorAll('input')].some(e=>e.disabled))throw Error('normal inputs still locked');})()`);
  console.log(file+': two cases and unlock passed');
 }
 // Inspect representative desktop and narrow layouts and save review images.
 for(const [prefix,c] of [['4-1-',2],['3-7-',2],['6-1-',1],['0-4-',1],['5-3-',1]]){
  const file=files.find(f=>path.basename(f).startsWith(prefix));
  await call('Page.navigate',{url:pathToFileURL(path.join(root,'lessons',file)).href+'?mistake='+c});
  await evaluate(`new Promise(r=>setTimeout(r,350))`);
  await evaluate(`(()=>{const r=document.querySelector('.demo');for(let i=0;i<3&&!r.querySelector('[data-action=next]').disabled;i++)r.querySelector('[data-action=next]').click();r.scrollIntoView({block:'start'})})()`);
  const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(__dirname,'.checks','process-'+prefix+'.png'),Buffer.from(shot.data,'base64'));
 }
 await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:false});
 await evaluate(`new Promise(r=>setTimeout(r,250))`);
 const mobile=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(__dirname,'.checks','process-mobile.png'),Buffer.from(mobile.data,'base64'));
 // Normal BFS records, DFS predecessors, and automatic pause at a warning.
 for(const prefix of ['3-3-','3-6-','3-7-']){
  const file=files.find(f=>path.basename(f).startsWith(prefix));await call('Page.navigate',{url:pathToFileURL(path.join(root,'lessons',file)).href});
  await evaluate(`new Promise(r=>setTimeout(r,200))`);
  await evaluate(`(()=>{const r=document.querySelector('.demo');for(let i=0;i<2;i++)r.querySelector('[data-action=next]').click();if(!r.querySelector('.graph-node-meta,.cell-parent'))throw Error('normal search records missing')})()`);
 }
 const binary=files.find(f=>path.basename(f).startsWith('1-1-'));await call('Page.navigate',{url:pathToFileURL(path.join(root,'lessons',binary)).href+'?mistake=1'});
 await evaluate(`new Promise(r=>setTimeout(r,200))`);
 await evaluate(`document.querySelector('[data-action=play]').click()`);
 await evaluate(`new Promise(r=>setTimeout(r,2100))`);
 if(!await evaluate(`!!document.querySelector('.mistake-alert')&&document.querySelector('[data-action=play]').textContent==='自动播放'`))throw Error('autoplay did not pause at error');
 if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({cases:count,frames,errors:errors.length}));ws.close();
}
main().catch(e=>{console.error(e);process.exit(1)});
