const { chromium } = require('playwright'); const path=require('path');
(async () => {
  const b = await chromium.launch();
  for (const lang of (process.env.LANGS || 'en ko ja').split(' ')) {
  const p = await b.newPage({ viewport:{width:1600,height:1000}, deviceScaleFactor: 1.5 });
  await p.goto('file://'+path.join(__dirname,'problem.html')+'?lang='+lang+'#still',{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(() => { document.querySelector('#cam').style.transition='none'; const g=document.getElementById('grid'); for(let i=0;i<100;i++){const d=document.createElement('div'); d.className='th on'; d.innerHTML='<div class="t"></div><div class="l"></div><div class="l" style="width:80%"></div><div class="l" style="width:60%"></div>'; g.appendChild(d);} document.getElementById('empty').style.opacity=0; document.getElementById('slide').classList.add('on'); });
  const shots=[['h1','off-the-point',null],['h2','generic',null],['h3','scattered','h4']];
  for (const [id,name,keep] of shots){
    const clip = await p.evaluate(({id,keep}) => {
      const s=document.getElementById('slide'); s.classList.add('focus'); document.querySelectorAll('.hl').forEach(e=>e.classList.remove('on','keep'));
      document.getElementById(id).classList.add('on'); if(keep) document.getElementById(keep).classList.add('keep');
      camEl(document.getElementById(id), 60);
      const r=document.getElementById(id).getBoundingClientRect();
      // 16:10 box around the element with padding, clamped to viewport
      let w=r.width+140, h=w*10/16; if(h<r.height+120){h=r.height+120; w=h*16/10;}
      let x=r.left+r.width/2-w/2, y=r.top+r.height/2-h/2-20;
      x=Math.max(0,Math.min(x,1600-w)); y=Math.max(0,Math.min(y,1000-h)); w=Math.min(w,1600); h=Math.min(h,1000);
      return {x,y,width:w,height:h};
    }, {id,keep});
    await p.waitForTimeout(400);
    await p.screenshot({path:`still-${name}.${lang}.png`, clip});
  }
  await p.close();
  }
  await b.close();
})();
