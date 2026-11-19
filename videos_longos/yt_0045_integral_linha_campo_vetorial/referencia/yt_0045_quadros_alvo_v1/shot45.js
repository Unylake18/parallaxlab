const {chromium}=require('playwright');const path=require('path');
const L=[["01_H1_helice_lata", "h1"], ["02_H2_ao_longo", "h2"], ["03_B1_forca_constante", "b1"], ["04_B2-1_particao", "b21"], ["05_B2-2_soma_riemann", "b22"], ["06_B3_definicao", "b3"], ["07_B4-1_redemoinho", "b41"], ["08_B4-2_soma_na_mao", "b42"], ["09_B4-3_no_raio", "b43"], ["10_B5-1_vento_para_fora", "b51"], ["11_B5-2_por_que_zero", "b52"], ["12_B6-1_outra_notacao", "b61"], ["13_B6-2_elipse", "b62"], ["14_B7-1_helice_montando", "b71"], ["15_B7-2_helice_conta", "b72"], ["16_B7-3_lendo_resposta", "b73"], ["17_S1_sintese", "s1"], ["18_S2_proximo", "s2"]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'||m.type()==='log')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb45.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:30000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
