const fs = require('fs'), path = require('path'), {pathToFileURL} = require('url');
let playwright; try { playwright = require('playwright'); } catch { playwright = require(path.join(process.env.NODE_REPL_NODE_MODULE_DIRS, 'playwright')); }
(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await playwright.chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page = await browser.newPage();
  try {
    const ids = [];
    for (let stage=0; stage<=6; stage++) {
      const files=fs.readdirSync(path.join(root,'codes',`stage-${stage}`));
      for(const file of files.filter(x=>/^\d+-\d+-.*\.html$/.test(x))) ids.push(file.match(/^\d+-\d+/)[0]);
    }
    for (const id of ids) {
      const dir = path.join(root, 'codes', `stage-${id[0]}`);
      const file = fs.readdirSync(dir).find(x => x.startsWith(id + '-') && x.endsWith('.html'));
      await page.goto(pathToFileURL(path.join(dir, file)).href);
      const cards = page.locator('.mistake-example');
      if (await cards.count() !== 2) throw Error(`${id}: wrong card count`);
      for (let i = 0; i < 2; i++) {
        await page.goto(pathToFileURL(path.join(dir, file)).href);
        const card = page.locator('.mistake-example').nth(i);
        if (await card.locator('pre code').count() !== 2) throw Error(`${id}: missing code`);
        await card.locator('a').click();
        await page.waitForSelector('.demo');
        let warning = false;
        for (let step = 0; step < 6; step++) {
          if (await page.locator('.mistake-alert').count()) warning = true;
          const next = page.locator('[data-action=next]');
          if (await next.isDisabled()) break;
          await next.click();
        }
        if (!warning) throw Error(`${id}/${i+1}: no error warning`);
      }
      console.log(`${id}: both code examples and warnings passed`);
    }
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
