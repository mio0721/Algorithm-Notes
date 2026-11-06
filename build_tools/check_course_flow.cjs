const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
let api;try{api=require('playwright');}catch(error){api=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'));}
(async()=>{
 const browser=await api.chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--no-sandbox','--disable-gpu']});
 const root=path.resolve(__dirname,'..'),shots=path.join(__dirname,'.checks');fs.mkdirSync(shots,{recursive:true});
 try{
  const context=await browser.newContext({viewport:{width:1500,height:1000},hasTouch:true,permissions:['clipboard-read','clipboard-write']}),page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  let count=0;
  for(let stage=0;stage<=6;stage++){
   const dir=path.join(root,'lessons',`stage-${stage}`);
   for(const file of fs.readdirSync(dir).filter(s=>s.endsWith('.html'))){
    await page.goto(pathToFileURL(path.join(dir,file)).href);
    await page.evaluate(()=>MathJax.startup.promise);
    if(await page.locator('.main .code-block').count())throw Error('lesson still embeds program: '+file);
    if(!await page.locator('.story-example').count())throw Error('missing concrete example: '+file);
    if(!await page.evaluate(()=>{
     const demo=document.querySelector('.demo');
     return [...document.querySelectorAll('.main .math-inline,.main .math-display')].every(el=>Boolean(demo.compareDocumentPosition(el)&Node.DOCUMENT_POSITION_FOLLOWING));
    }))throw Error('formula before demo: '+file);
    if(await page.locator('[data-mml-node="merror"]').count())throw Error('formula error: '+file);
    const codeURL=await page.locator('.implementation-button').getAttribute('href');
    await page.goto(new URL(codeURL,page.url()).href);
    await page.evaluate(()=>MathJax.startup.promise);
    for(const language of ['cpp','python']){
     await page.locator(`[data-language="${language}"]`).click();
     if(await page.locator('.code-language-panel:visible').count()!==1)throw Error('two languages visible: '+file);
     const panel=page.locator(`[data-code-language="${language}"]`);
     if(!await panel.isVisible())throw Error('wrong active language: '+file);
     const source=await panel.locator('.code-block code').textContent();
     const link=await panel.locator('a[download]').getAttribute('href');
     const codefile=path.join(root,'codes',`stage-${stage}`,link);
     if(source.replace(/\r\n/g,'\n')!==fs.readFileSync(codefile,'utf8').replace(/\r\n/g,'\n'))throw Error('copy/download mismatch: '+file);
     if(!/[\u4e00-\u9fff]/.test(source))throw Error('Chinese comments missing: '+file);
    }
    if(file.startsWith('1-1')){
     await page.locator('[data-language="cpp"]').click();
     if(await page.locator('#code-panel-cpp .teaching-table tbody tr').count()!==2)throw Error('binary search has unused headers');
     await page.screenshot({path:path.join(shots,'course-code-tabs-desktop.png'),fullPage:true});
     await page.setViewportSize({width:390,height:844});
     await page.locator('[data-language="python"]').tap();
     if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2))throw Error('mobile code overflow');
     await page.screenshot({path:path.join(shots,'course-code-tabs-mobile.png')});
     await page.setViewportSize({width:1500,height:1000});
    }
    count++;
   }
   console.log('Example-first lessons and language-switch code pages passed: stage',stage);
  }
  if(errors.length)throw Error(errors.join('\n'));
  console.log(`${count} lessons: concrete examples before demo, theory after demo, no embedded program; 90 code/download views matched.`);
  await context.close();
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
