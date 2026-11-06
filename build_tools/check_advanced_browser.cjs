const path = require('path');
const fs = require('fs');
const {pathToFileURL} = require('url');
let playwright;
try { playwright=require('playwright'); }
catch(error) {
  if(!process.env.NODE_REPL_NODE_MODULE_DIRS)throw error;
  playwright=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'));
}
const {chromium}=playwright;
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-crash-reporter', '--disable-breakpad']
  });
  try {
    const page = await browser.newPage({viewport: {width: 1500, height: 1000}});
    const errors=[];
    page.on('pageerror', e=>errors.push(e.message));
    const root=path.resolve(__dirname,'..');
    for (const stage of [4,5,6]) {
      const dir=path.join(root,'lessons',`stage-${stage}`);
      for (const name of fs.readdirSync(dir).filter(s=>s.endsWith('.html'))) {
        await page.goto(pathToFileURL(path.join(dir,name)).href);
        await page.locator('.advanced-controls select').first().waitFor();
        const status=page.locator('.demo .status');
        if(!/1 \/ \d+/.test(await status.innerText()))throw Error(`no frames: ${name}`);
        for(let preset=0;preset<3;preset++){
          await page.locator('.advanced-controls select').first().selectOption(String(preset));
          const button=page.locator('[data-action=next]');
          const before=await button.evaluate(el=>el.getBoundingClientRect().top+window.scrollY);
          const total=Number((await status.innerText()).match(/\/ (\d+)/)[1]);
          await button.evaluate((el,count)=>{for(let step=1;step<count;step++)el.click();},total);
          const after=await button.evaluate(el=>el.getBoundingClientRect().top+window.scrollY);
          if(Math.abs(after-before)>2)throw Error(`button moved: ${name}: ${before} -> ${after}`);
          if(name.startsWith('4-6')&&preset===2&&await page.locator('.dp-matrix').count())throw Error('empty input retained previous matrix');
        }
        console.log('Browser passed:',name.slice(0,3));
        if(name.startsWith('6-4')){
          await page.locator('.advanced-controls select').first().selectOption('0');
          await page.locator('[data-action=next]').evaluate(el=>{for(let i=0;i<80;i++)el.click();});
          fs.mkdirSync(path.join(__dirname,'.checks'),{recursive:true});
          await page.locator('.demo').screenshot({path:path.join(__dirname,'.checks','algorithm-rrt-star.png')});
        }
      }
    }
    // Exercise editable maps, actual A*/uniform-cost results and narrow layouts.
    const mapPage=fs.readdirSync(path.join(root,'lessons','stage-6')).find(s=>s.startsWith('6-1'));
    await page.goto(pathToFileURL(path.join(root,'lessons','stage-6',mapPage)).href);
    await page.locator('.advanced-controls select').first().selectOption('1');
    await page.locator('[data-grid-row="2"][data-grid-col="3"]').click();
    await page.getByRole('button',{name:'计算路径',exact:true}).click();
    await page.locator('[data-action=next]').evaluate(el=>{for(let i=0;i<200;i++)el.click();});
    if(await page.locator('.map-cell.route').count()<2)throw Error('custom route not highlighted');
    await page.locator('.advanced-controls select').nth(2).selectOption('8,8');
    if(await page.locator('.map-cell').count()!==64)throw Error('shape not applied');
    await page.getByRole('button',{name:'计算路径',exact:true}).click();
    const totals=[];
    for(const method of ['astar','uniform']){
      await page.locator('.advanced-controls select').nth(3).selectOption(method);
      await page.getByRole('button',{name:'计算路径',exact:true}).click();
      await page.locator('[data-action=next]').evaluate(el=>{for(let i=0;i<200;i++)el.click();});
      totals.push(await page.locator('.step-text').innerText());
    }
    if(!totals.every(s=>s.includes('14 步')))throw Error('A* and uniform mismatch');
    await page.evaluate(()=>document.documentElement.dataset.theme='dark');
    await page.setViewportSize({width:390,height:844});
    await page.waitForTimeout(300);
    if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2))throw Error('mobile horizontal overflow');
    await page.locator('.demo').screenshot({path:path.join(__dirname,'.checks','algorithm-map-mobile.png')});
    console.log('Custom maps, path highlights, dark theme and mobile layout passed.');
    if(errors.length)throw Error(errors.join('\n'));
  } finally {await browser.close();}
})().catch(error=>{console.error(String(error));process.exitCode=1;});
