const {chromium}=require('playwright');const path=require('path');
const L=[['01_H1_bola_pesada_trava','h1'],['02_H2_grade_nova_dois_pedacos','h2'],['03_B1-1_endereco_esferico','b1'],['04_B1-2_ponto_de_exemplo','b1b'],['05_B1-3_caixa_vira_bola','b13'],
['06_B2-1_caixinha_tres_arestas','b21'],['07_B2-2_duas_polares','b22'],['08_B2-3_determinante','b23'],['09_B2-4_teste_da_bola','b24'],['10_B3-1_teorema','b31'],['11_B4_cebola','b4'],['12_B5_bola_pesada_M_pi','b5'],['13_B6_casquinha','b6'],['14_S2_lata_gancho','s2']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const only=process.argv.slice(2);for(const [n,k] of L){if(only.length&&!only.includes(k))continue;errs.length=0;await p.goto('file://'+path.resolve('sb41.html')+'?k='+k);
 try{await p.waitForFunction(()=>document.title==='ok',null,{timeout:20000});}catch(e){console.log('TIMEOUT',k,errs.join('|'));continue;}
 await p.screenshot({path:n+'.jpg',type:'jpeg',quality:90});if(errs.length)console.log(k,errs.join('|'));}
await b.close();})();
