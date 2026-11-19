const {chromium}=require('playwright');const path=require('path');
const L=[['v3_01_abertura_faca_em_pe','v3_c1'],['v3_02_abertura_faca_deitada','v3_c2'],['v3_03_B1-3_raiz_do_desenho_e_trig','v3_b13'],['v3_04_B3-2_funcoes_area_cunha','v3_b3A'],['v3_05_B4-2_funcoes_area_sino','v3_b42A'],['v3_06_B4-2_passo3_substituicao','v3_b42c'],['v3_07_S2_saida_troca_e_cartao','v3_s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb34v3.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
