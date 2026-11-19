const {chromium}=require('playwright');const path=require('path');
const L=[['01_H_a_integral_que_nao_colabora','h0'],['02_B1_plano_rtheta_vira_disco','b1'],['03_B2_retangulo_polar_setores','b2'],['04_B2_jacobiano_e_erro_classico','b2j'],['05_B3_teorema_duas_metades','b3'],['06_B4_o_disco_do_comeco','h1'],['07_B5_disco_deslocado_r_2cos','b6'],['08_B6_gauss_confronto','b7'],['09_S_gancho_meio_disco','s2']];
const L1=[['01_H1_fator_da_grade_de_circulos','h1'],['02_B1_plano_rtheta_vira_disco','b1'],['03_B2_retangulo_polar_setores','b2'],['04_B2_jacobiano_e_erro_classico','b2j'],
['05_B4_meio_disco_sen_r2','b4'],['06_B5_esfera_em_cascas','b5'],['07_B6_disco_deslocado_r_2cos','b6'],['08_B7_gauss_confronto','b7'],['09_S2_gancho_meia_lua','s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb34t2.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
