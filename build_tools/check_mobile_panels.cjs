const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
let api;try{api=require('playwright');}catch(error){api=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'));}
const algo=path.resolve(__dirname,'..'),control=path.resolve(algo,'../../Control/Control-Engineering-Notes');
const output=path.join(__dirname,'.checks');fs.mkdirSync(output,{recursive:true});
function lesson(root,stage,prefix){const dir=path.join(root,'lessons',`stage-${stage}`);return path.join(dir,fs.readdirSync(dir).find(s=>s.startsWith(prefix)));}
(async()=>{
 const browser=await api.chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--no-sandbox','--disable-gpu']});
 try{
  const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}),page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  const cdp=await context.newCDPSession(page);
  const swipe=async(x,start,end)=>{
   await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y:start}]});
   for(let i=1;i<=8;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:start+(end-start)*i/8}]});
   await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(120);
  };
  const visit=async(file)=>{
   await page.goto(pathToFileURL(file).href);await page.locator('.mobile-toolbar').waitFor();
   await page.evaluate(()=>window.MathJax?.startup?.promise);await page.waitForTimeout(80);
   if(await page.locator('.layout>.sidebar').isVisible())throw Error('sidebar still pushes mobile lesson down');
   if(await page.locator('.layout>.problem-rail').count()&&await page.locator('.layout>.problem-rail').isVisible())throw Error('practice still appears below lesson');
  };
  for(const [name,file,secondary] of [
   ['algorithm',lesson(algo,3,'3-1'),'本节练习'],
   ['control',path.join(control,'lessons',fs.readdirSync(path.join(control,'lessons')).find(s=>s.startsWith('01-'))),'本页目录']
  ]){
   await visit(file);
   await page.evaluate(()=>scrollTo({top:500,behavior:'instant'}));await page.waitForTimeout(100);
   const saved=await page.evaluate(()=>scrollY),position=await page.locator('.main').evaluate(el=>el.getBoundingClientRect().top);
   await page.locator('.mobile-toolbar').getByRole('button',{name:'课程目录',exact:true}).tap();
   await page.locator('dialog[open]').waitFor();
   if(await page.evaluate(()=>document.body.style.position)!=='fixed')throw Error('background not locked');
   const body=page.locator('.mobile-sheet-body');await body.evaluate(el=>el.scrollTop=0);
   await swipe(190,690,260);
   if(await body.evaluate(el=>el.scrollTop)<=0)throw Error('touch cannot scroll directory');
   await body.evaluate(el=>el.scrollTop=el.scrollHeight);await swipe(190,690,260);
   const after=await page.locator('.main').evaluate(el=>el.getBoundingClientRect().top);
   if(Math.abs(after-position)>2)throw Error('background moved during directory touch');
   await page.locator('.mobile-sheet-tabs').getByRole('button',{name:secondary,exact:true}).tap();
   if(!await page.locator(secondary==='本节练习'?'.mobile-sheet .problem-rail':'.mobile-sheet .toc').isVisible())throw Error('secondary pane missing');
   await page.getByRole('button',{name:'关闭面板',exact:true}).tap();await page.waitForTimeout(100);
   if(Math.abs(await page.evaluate(()=>scrollY)-saved)>2)throw Error(`close did not restore lesson position ${name}: ${saved} -> ${await page.evaluate(()=>scrollY)}`);
   await page.locator('.mobile-toolbar').getByRole('button',{name:secondary,exact:true}).tap();
   await page.screenshot({path:path.join(output,`${name}-mobile-panel.png`)});
   if(name==='control'){
    const anchor=page.locator('.mobile-sheet .toc a[href^="#"]').first(),href=await anchor.getAttribute('href');await anchor.tap();await page.waitForTimeout(150);
    if(await page.locator('.mobile-sheet').evaluate(el=>el.open))throw Error('toc navigation did not close');
    if(await page.evaluate(()=>location.hash)!==href)throw Error('toc navigation failed');
   }else{await page.keyboard.press('Escape');await page.waitForTimeout(100);}
   await page.setViewportSize({width:900,height:1000});if(!await page.locator('.mobile-toolbar').isVisible())throw Error('tablet toolbar missing');
   await page.locator('.mobile-toolbar').getByRole('button',{name:'课程目录',exact:true}).tap();
   await page.setViewportSize({width:1500,height:1000});await page.waitForTimeout(100);
   if(await page.locator('.mobile-sheet').evaluate(el=>el.open))throw Error('resize did not close drawer');
   if(!await page.locator('.layout>.sidebar').isVisible())throw Error('desktop directory not restored');
   if(await page.evaluate(()=>document.body.style.position)==='fixed')throw Error('body stayed locked');
   await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(100);
   if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2))throw Error('mobile horizontal overflow');
   await page.screenshot({path:path.join(output,`${name}-mobile-topbar.png`)});
   console.log(name,'touch panel, background lock, navigation, scroll restoration and desktop resize passed');
  }
  await visit(lesson(algo,5,'5-3'));
  if(await page.locator('[data-grid-row="0"][data-grid-col="8"] .cell-metric').count())throw Error('undiscovered A* metrics exposed');
  if(await page.locator('[data-grid-row="0"][data-grid-col="0"] .cell-metric').count()!==3)throw Error('start A* metrics missing');
  await page.locator('[data-action=next]').evaluate(el=>el.click());
  if(!await page.locator('[data-grid-row="1"][data-grid-col="0"] .cell-metric').count())throw Error('discovered metrics did not appear');
  if(await page.locator('.cell-metric').filter({hasText:/^w 1$/}).count())throw Error('uniform weights repeated in cells');
  await page.locator('[data-action=prev]').evaluate(el=>el.click());
  if(await page.locator('[data-grid-row="1"][data-grid-col="0"] .cell-metric').count())throw Error('rewind retained future metrics');
  console.log('Progressive grid metrics, uniform weight legend and rewind passed');
  if(errors.length)throw Error(errors.join('\n'));
  await context.close();
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
