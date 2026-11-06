const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
let p;try{p=require('playwright')}catch{p=require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS,'playwright'))}
(async()=>{const root=path.resolve(__dirname,'..'),browser=await p.chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'}),page=await browser.newPage();
try{
  async function open(stage,prefix){const dir=path.join(root,'lessons',`stage-${stage}`),name=fs.readdirSync(dir).find(x=>x.startsWith(prefix+'-')&&x.endsWith('.html'));await page.goto(pathToFileURL(path.join(dir,name)).href)}
  await open(1,'1-1');
  const input=page.locator('[data-input=array]'),preset=page.locator('[data-input=preset]');
  const original=await input.inputValue();await preset.selectOption('__mistake__1');
  if(await input.inputValue()!=='1, 3, 5'||!await input.isDisabled())throw Error('mistake array not synchronized and locked');
  await preset.selectOption('__mistake__2');
  if(await input.inputValue()!=='8, 2, 6')throw Error('second case array not synchronized');
  await preset.selectOption('default');
  if(await input.isDisabled()||await input.inputValue()!==original)throw Error('normal array not restored');
  await open(3,'3-6');
  await page.locator('[data-action=next]').click();
  if(!await page.locator('.graph-node-meta').count())throw Error('BFS node metadata missing');
  await open(4,'4-1');
  const scenario=page.locator('.advanced-controls select').first();await scenario.selectOption('__mistake__2');
  if(!await page.locator('.advanced-diagram').count())throw Error('backtracking error tree missing');
  if(await scenario.isDisabled())throw Error('case selector disabled');
  console.log('Array sync/unlock, BFS metadata and backtracking tree passed.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
