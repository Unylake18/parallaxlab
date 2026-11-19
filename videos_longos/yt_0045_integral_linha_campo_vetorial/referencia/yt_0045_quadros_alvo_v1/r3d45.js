const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:1920,height:1080}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const out={};for(const k of process.argv.slice(2)){await p.goto('file://'+path.resolve('c3d45.html')+'?k='+k);await p.waitForFunction(()=>document.title==='ok',null,{timeout:120000});
 await p.screenshot({path:'r3d_'+k+'.png',omitBackground:true});out[k]=await p.evaluate(()=>window.PTS);}
if(errs.length)console.log(errs.join('\n'));
let old={};try{old=JSON.parse(fs.readFileSync('r3d_pts.json'))}catch(e){};Object.assign(old,out);fs.writeFileSync('r3d_pts.json',JSON.stringify(old,null,1));fs.writeFileSync('r3d_pts.js','window.R3D='+JSON.stringify(old)+';');
await b.close();})();
