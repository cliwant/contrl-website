const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const outDir = path.join(__dirname, 'out_hd'); fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 3200, height: 2000 }, deviceScaleFactor: 1, recordVideo: { dir: outDir, size: { width: 3200, height: 2000 } } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.join(__dirname, process.env.PAGE || 'replay.html') + '?hd&lang=' + (process.env.LANG_CODE || 'en') + (process.env.NOCAP ? '&nocap' : ''), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(Number(process.env.DURATION_MS || 46000));
  const video = page.video(); await ctx.close(); const p = await video.path();
  fs.renameSync(p, path.join(outDir, (process.env.OUTNAME || 'raw') + '.webm')); await browser.close(); console.log('done');
})();
