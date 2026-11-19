const {chromium}=require('playwright');const path=require('path');
const L=[['01_H1_bola_octante_v2','h1v2'],['03_B1-1_endereco_duas_vistas_v2','b1v2'],['07_B2-2_duas_polares_v2','b22v2'],['08a_B2-3_menores_v2','b23v2'],['08b_B2-3_expansao_v2','b23bv2'],['10b_B3-2_receita_v2','b32'],['11_B4_cebola_octante_v2','b4v2'],['12_B5_massa_ate_c_v2','b5v2'],['13a_B6-1_casquinha_corte_v2','b61'],['13b_B6-2_substituicao_v2','b62'],['14_S2_lata_corte_v2','s2v2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb41.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
