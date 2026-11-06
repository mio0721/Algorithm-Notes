const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
let api;try{api=require('playwright');}catch(error){api=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'));}
(async()=>{
  const browser=await api.chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--no-sandbox','--disable-gpu']});
  const root=path.resolve(__dirname,'..'),output=path.join(__dirname,'.checks');fs.mkdirSync(output,{recursive:true});
  let mathCount=0,pages=0;
  try{
    const page=await browser.newPage({viewport:{width:1500,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
    const open=async(stage,prefix)=>{
      const dir=path.join(root,'lessons',`stage-${stage}`),name=fs.readdirSync(dir).find(n=>n.startsWith(prefix));
      await page.goto(pathToFileURL(path.join(dir,name)).href);
      await page.evaluate(()=>window.MathJax.startup.promise);
    };
    for(let stage=0;stage<=6;stage++){
      const dir=path.join(root,'lessons',`stage-${stage}`);
      for(const name of fs.readdirSync(dir).filter(n=>n.endsWith('.html'))){
        await page.goto(pathToFileURL(path.join(dir,name)).href);
        await page.evaluate(()=>window.MathJax.startup.promise);
        const failures=await page.locator('[data-mml-node="merror"],mjx-merror').count();
        if(failures)throw Error(`MathJax errors in ${name}`);
        const inline=await page.locator('.math-inline').count(),rendered=await page.locator('.math-inline mjx-container').count();
        if(inline!==rendered)throw Error(`unrendered inline formula in ${name}: ${inline}/${rendered}`);
        const indent=await page.locator('.story-example p').evaluate(el=>({indent:parseFloat(getComputedStyle(el).textIndent),font:parseFloat(getComputedStyle(el).fontSize)}));
        if(Math.abs(indent.indent-indent.font*2)>0.1)throw Error(`paragraph indent incorrect: ${name}`);
        mathCount+=await page.locator('mjx-container').count();pages++;
      }
      console.log('Math and indentation passed: stage',stage);
    }
    await open(6,'6-4');
    if(!await page.locator('.math-display [data-mml-node="msqrt"]').count()||!await page.locator('.math-display [data-mml-node="mfrac"]').count())throw Error('radius not typeset as sqrt/fraction');
    await page.locator('.math-display').first().screenshot({path:path.join(output,'rrt-radius-math.png')});
    for(const [stage,prefix,labels] of [[5,'5-3',['g 0','h 13','f 13']],[6,'6-2',['g','rhs']],[3,'3-8',['d']],[3,'3-7',['深度']]]){
      await open(stage,prefix);
      if(stage===3)await page.locator('[data-action=next]').evaluate(el=>el.click());
      await page.locator('.cell-metric').first().waitFor();
      const first=await page.locator(prefix==='6-2'?'[data-grid-row="5"][data-grid-col="8"]':'[data-grid-row="0"][data-grid-col="0"]').innerText();
      if(!labels.every(label=>first.includes(label)))throw Error(`missing metrics ${prefix}: ${first}`);
      const before=await page.locator('[data-action=next]').evaluate(el=>el.getBoundingClientRect().top+scrollY);
      await page.locator('[data-action=next]').evaluate(el=>{for(let i=0;i<12;i++)el.click();});
      const after=await page.locator('[data-action=next]').evaluate(el=>el.getBoundingClientRect().top+scrollY);
      if(Math.abs(after-before)>2)throw Error(`grid playback moved buttons: ${prefix}`);
    }
    await open(5,'5-3');
    await page.locator('[data-action=next]').evaluate(el=>{for(let i=0;i<8;i++)el.click();});
    await page.locator('.demo').screenshot({path:path.join(output,'astar-cell-scores.png')});
    await page.evaluate(()=>document.documentElement.dataset.theme='dark');
    await page.setViewportSize({width:390,height:844});await page.waitForTimeout(300);
    if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2))throw Error('mobile page overflow');
    if(!await page.locator('.grid-scroll').evaluate(el=>el.scrollWidth>el.clientWidth))throw Error('narrow grid should scroll internally');
    await page.locator('.demo').screenshot({path:path.join(output,'astar-cell-scores-mobile.png')});
    await open(6,'6-4');
    if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2)){
      console.log(await page.evaluate(()=>[...document.querySelectorAll('.main,.main p,.math-inline,.math-display,.main mjx-container')].filter(el=>el.getBoundingClientRect().right>innerWidth+2).map(el=>({tag:el.tagName,cls:el.className,width:el.getBoundingClientRect().width,right:el.getBoundingClientRect().right,text:el.textContent.slice(0,90)})).slice(0,15)));
      throw Error('mobile formula page overflow');
    }
    if(errors.length)throw Error(errors.join('\n'));
    console.log(`${pages} lesson pages, ${mathCount} rendered formulas: no MathJax errors. Grid metrics, playback and mobile checks passed.`);
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
