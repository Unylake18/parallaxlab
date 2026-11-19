const {chromium}=require('playwright');const path=require('path');
const L=[['v3_01_H2_promessa_sino','v3h2'],['v3_02_S1_paineis_juntos','v3sint'],['v3_03_S2_gancho_massa','v3gancho']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
for(const [n,k] of L){errs.length=0;await p.goto('file://'+path.resolve('sb34t3.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
