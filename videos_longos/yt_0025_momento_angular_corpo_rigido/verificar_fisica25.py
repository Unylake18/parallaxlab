"""QA físico independente: diferenças finitas, torques por forças e critérios do handoff."""
import json
import math
import numpy as np
from pathlib import Path
import fisica25 as F
U=Path(__file__).resolve().parent
resultados=[]
def check(nome,erro,limite,unidade=''):
    resultados.append(dict(nome=nome,erro=float(erro),limite=limite,unidade=unidade,ok=bool(erro<=limite)))
maximos=dict(pend_ort=0.,pend_torque=0.,pend_mod=0.,hal_ort=0.,hal_torque=0.,mancal=0.,sinal=0.,x=0.,voxel=0.)
for ph in np.linspace(0,2*np.pi,121):
    p,h=F.pendulo(ph),F.haltere(ph)
    dt=1e-5
    deriv=(F.pendulo(ph+F.WP*dt)['L']-F.pendulo(ph-F.WP*dt)['L'])/(2*dt)
    maximos['pend_ort']=max(maximos['pend_ort'],abs(F.ang(p['L'],p['r'])-90))
    maximos['pend_torque']=max(maximos['pend_torque'],np.linalg.norm(deriv-np.cross(p['r'],[0,0,-.2*9.8])))
    maximos['pend_mod']=max(maximos['pend_mod'],abs(np.linalg.norm(p['L'])-.3363935979788656))
    maximos['hal_ort']=max(maximos['hal_ort'],abs(F.ang(h['L'],h['r'])-90))
    torquef=np.cross(h['massa'],h['Fc'])+np.cross(h['massa2'],h['Fc2'])
    maximos['hal_torque']=max(maximos['hal_torque'],np.linalg.norm(torquef-h['torque']))
    tauA=np.cross([0,0,-.45],h['Fsup'])+np.cross([0,0,-.85],h['Finf'])
    maximos['mancal']=max(maximos['mancal'],np.linalg.norm(tauA-h['torque']))
    if np.dot(h['transversal'],h['massa2'])<0:maximos['sinal']=1
    maximos['x']=max(maximos['x'],np.linalg.norm(F.haltere(ph,1)['transversal']))
    v=F.voxel(ph,1);maximos['voxel']=max(maximos['voxel'],F.ang(v['L'],F.Z))
check('PÊNDULO L perpendicular ao fio',maximos['pend_ort'],1,'grau')
check('PÊNDULO dL/dt = torque do peso',maximos['pend_torque'],1e-6,'N m')
check('PÊNDULO módulo constante',maximos['pend_mod'],.336*.005,'kg m²/s')
check('HALTERE L perpendicular à haste',maximos['hal_ort'],1,'grau')
check('HALTERE torque pelas centrípetas',maximos['hal_torque'],1e-6,'N m')
check('MANCAIS binário e direção',maximos['mancal'],1e-6,'N m')
check('SINAIS transversal para a massa de baixo',maximos['sinal'],0)
check('X transversal total',maximos['x'],.01*.113)
check('VOXEL principal após remontagem',maximos['voxel'],.5,'grau')
check('VOXEL CM no eixo',np.linalg.norm(np.array(F.VOX['posicoes']).mean(axis=0)),.001,'m')
antes=F.ang(F.voxel(0)['L'],F.Z)
check('VOXEL inclinação inicial >= 20 graus',max(0,20-antes),0,'grau')
I=np.array(F.VOX['tensor']);n0=np.array(F.VOX['inicial']).T@F.Z;ev=np.array(F.VOX['eixos'])
menor=min(min(F.ang(n0,ev[:,i]),180-F.ang(n0,ev[:,i])) for i in range(3))
check('VOXEL eixo principal mais próximo 35 ± 5 graus',abs(menor-35),5,'grau')
p=np.array([[.2,.1,0],[-.2,-.1,0],[-.2,.1,0],[.2,-.1,0]])
check('RODA CM dos excessos no eixo',np.linalg.norm(p[:2].mean(axis=0)),1e-12,'m')
check('RODA produtos de inércia após contrapesos',max(abs(np.sum(p[:,0]*p[:,1]*.02)),abs(np.sum(p[:,2]*p[:,1]*.02))),1e-12,'kg m²')
check('RODA aliasing aparente 18 graus/quadro',max(0,1.5*math.pi/15*180/math.pi-30),0,'grau')
p=F.pendulo(0);rc=p['massa']-np.array([0.,0.,-math.cos(F.TH)]);lc=np.cross(rc,p['p'])
check('OUTRA ORIGEM L axial no centro do círculo',np.linalg.norm(lc[:2]),1e-12)
check('OUTRA ORIGEM Lz = 0,1682',abs(lc[2]-.1682)/.1682,.005)
tracao=-.2*9.8/math.cos(F.TH)*p['r']
check('OUTRA ORIGEM torques do peso e da tração se cancelam',np.linalg.norm(np.cross(rc,-.2*9.8*F.Z)+np.cross(rc,tracao)),1e-12)
erros=[]
for ph in np.linspace(0,2*np.pi,61):
    roda=F.roda(ph)
    binario=np.cross([0,.25,0],roda['Fa1'])+np.cross([0,-.25,0],roda['Fa2'])
    erros.append(np.linalg.norm(binario-roda['torque']))
check('RODA binário pelos apoios',max(erros),1e-10,'N m')
h1,h3=F.haltere(0),F.haltere(0,multiplicador_omega=3)
check('SÍNTESE sem torque: s² omega constante',max(abs(s*s*w-math.pi) for s,ph,w in (F.deformacao(t) for t in np.linspace(0,12,121))),1e-12)
for k in ['torque','Fsup','Finf','Fc']:
    check('HALTERE triplicar omega multiplica '+k+' por nove',np.linalg.norm(h3[k]-9*h1[k]),1e-10)
for grupo,chave,valor in [('pendulo','omega',3.364),('pendulo','torque',.98),('haltere','Lz',.113),('haltere','Lperp',.196),('haltere','torque',1.23),('roda','Fc',34.3),('roda','binario',6.86)]:
    med=F.tabula()[grupo][chave];check(f'NÚMEROS {grupo} {chave}',abs(med-valor)/valor,.005,'relativo')
(U/'qa/fisica.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=1),encoding='utf-8')
for r in resultados:print(('OK' if r['ok'] else 'FALHA'),r['nome'],f"{r['erro']:.8g} {r['unidade']}")
raise SystemExit(0 if all(r['ok'] for r in resultados) else 1)
