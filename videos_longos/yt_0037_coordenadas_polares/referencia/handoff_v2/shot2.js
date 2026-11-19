const {chromium}=require('playwright');const path=require('path');
const L=[['v2_01_B4-2_casca_e_anel_inteiro','v2casca'],['v2_02_B2-3_teste_da_unidade','v2erro'],['v2_03_B6-2_entre_dois_discos','v2gauss'],['v2_04_B7_quadrado_duas_integrais','v2quad'],['v2_05_S1_sintese_tres_paineis','v2sint'],['v2_06_S2_gancho_meio_disco','v2gancho']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb34t2.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
