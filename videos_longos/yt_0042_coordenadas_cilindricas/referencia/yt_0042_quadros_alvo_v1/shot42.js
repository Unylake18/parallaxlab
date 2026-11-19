const {chromium}=require('playwright');const path=require('path');
const L=[['01_H1_lata_pesada','h1'],['02_H2_grade_da_lata','h2'],['03_B1-1_endereco','b11'],['04_B1-2_ponto','b12'],['05_B1-3_caixa_vira_lata','b13'],['06_B2-1_caixinha','b21'],['07_B2-2_polares_x_altura','b22'],['08_B2-3_determinante','b23'],['09_B2-4_teste_cilindro','b24'],['10_B3-1_teorema','b31'],['11_B4-1_fora_do_eixo_montar','b41'],['12_B4-2_fora_do_eixo_conta','b42'],['13_B5-2_integral_em_s','b52'],['14_B5-3_triangulo','b53'],['15_B5-4_secante_quinta','b54'],['16_B5-5_massa','b55'],['17_S2_girar_e_proximo','s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'||m.type()==='log')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb42.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:30000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
