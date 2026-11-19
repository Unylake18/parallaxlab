const {chromium}=require('playwright');const path=require('path');
const L=[['v1_01_H1_centro_no_buraco','h1'],['v1_02_E1-2_bordas_para_uv','e12'],['v1_03_E1-3_comprimento_cancela','e13'],['v1_04_E2-2_jacobiano_da_volta','e22'],['v1_05_E2-3_area_e_pipa','e23'],
['v1_06_E3-1_oitavo_de_bola_3d','e31'],['v1_07_E3-2_polares_quarto_de_disco','e32'],['v1_08_E4-1_polares_esticadas','e41'],['v1_09_E4-3_meia_elipse_centro','e43'],['v1_10_E5-2_centro_no_buraco','e52'],
['v1_11_E5-3_fio_de_prumo','e53'],['v1_12_E5-4_regua_homogenea_x_kr','e54'],['v1_13_E6-1_pappus_anel','e61'],['v1_14_E6-3_bola_oca_confere','e63'],['v1_15_S2_cubo_proximo','s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb39.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();console.log('fim');})();
