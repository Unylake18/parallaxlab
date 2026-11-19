const {chromium}=require('playwright');const path=require('path');
const L=[['v2_01_H1_trava_sino_area','v2_h1a'],['v2_02_H1_limites_mudaram','v2_h1b'],['v2_03_B1-1_R_com_folga','v2_b11'],['v2_04_B1-2_selos_com_titulo','v2_b12i'],['v2_05_B1-2_fatia_zero_f_zero','v2_b12'],['v2_06_B4-2_sino_inteiro','v2_b42p'],['v2_07_B4-3_comeco_anda','v2_b43a'],['v2_08_B4-3_resultado_com_x','v2_b43b'],['v2_09_B5-1_triangulo_B','v2_b51'],['v2_10_B6-1_paineis_na_coluna','v2_b61'],['v2_11_B7-1_leve_em_foco','v2_b71m'],['v2_12_B7-2_miniaturas','v2_b72'],['v2_13_S1_sintese','v2_s1'],['v2_14_S2_rotulo_dentro','v2_s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb34v2.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
