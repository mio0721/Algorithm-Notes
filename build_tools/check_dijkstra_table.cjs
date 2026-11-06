const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
let p;try{p=require('playwright')}catch{p=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'))}
(async()=>{
 const root=path.resolve(__dirname,'..'),dir=path.join(root,'lessons','stage-5');
 const file=fs.readdirSync(dir).find(f=>f.startsWith('5-2-')&&f.endsWith('.html'));
 const browser=await p.chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1500,height:900}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 try {
  await page.goto(pathToFileURL(path.join(dir,file)).href);
  const rows=page.locator('.network-state-table tbody tr');
  if(await rows.count()!==10)throw Error('expected 10 node rows');
  if(!(await rows.nth(0).innerText()).includes('已确定'))throw Error('start should be settled');
  if(!(await rows.nth(1).innerText()).includes('∞'))throw Error('B should initially be unreachable');
  await page.locator('[data-action=next]').click();
  if(!(await rows.nth(1).innerText()).includes('4'))throw Error('B distance should update to 4');
  if(!(await rows.nth(1).innerText()).includes('A'))throw Error('B parent should be A');
  await page.setViewportSize({width:390,height:844});
  const layout=await page.locator('.network-state-layout').evaluate(el=>getComputedStyle(el).gridTemplateColumns);
  if(layout.split(' ').length!==1)throw Error('mobile table should stack');
  if(errors.length)throw Error(errors.join('\n'));
  console.log('Dijkstra table updates and mobile layout passed.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
