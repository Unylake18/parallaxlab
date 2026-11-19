const {chromium}=require('playwright');const path=process.argv[2],out=process.argv[3],keys=process.argv.slice(4);
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1920,height:1080}});
 pg.on('pageerror',e=>console.log('ERR',e.message));pg.on('console',m=>{const t=m.text();if(t.startsWith('AUDIT')||m.type()==='error')console.log(t);});
 for(const k of keys){await pg.goto('file://'+path+'?k='+k);try{await pg.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k);}
  await pg.screenshot({path:`${out}/${k}.jpg`,type:'jpeg',quality:92});}
 await b.close();})();
