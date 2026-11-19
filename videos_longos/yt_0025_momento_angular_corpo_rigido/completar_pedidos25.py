"""Acrescenta as amostras das forças dos apoios da roda a estados físicos já medidos.

Só muda metadados de setas Manim: câmera, corpo, tempo e imagens Three.js permanecem os estados da passagem seca.
"""
import json
from pathlib import Path
import numpy as np
import fisica25 as F
from manim.utils.rate_functions import smooth
U=Path(__file__).resolve().parent
p=U/'threejs/pedidos3d/PB6.json';d=json.loads(p.read_text(encoding='utf-8'))
a=json.loads((U/'ancoras.json').read_text(encoding='utf-8'))['ancoras'];inicio=round((a['B6-3']['ini']-a['B6-1']['ini'])*15)
for f,e in d['cenas']['roda_balanceamento']:
    fis=F.roda(e['phi'],e['balanceada'])
    for k in ['L','axial','transversal','torque']:e['pontos'][k]=fis[k].round(4).tolist()
    for nome,vetor in [('L','L'),('Lh','transversal')]:
        if f'{nome}:0' in e['pontos']:
            for j,u in enumerate(np.linspace(0,1,25)):e['pontos'][f'{nome}:{j}']=(u*2.1*fis[vetor]).round(4).tolist()
    if f<inicio:continue
    for nome,z in [('Fa1',.25),('Fa2',-.25)]:
        base=np.array([0,z,0]);vet=fis[nome]*.018
        for j,u in enumerate(np.linspace(0,1,25)):e['pontos'][f'{nome}:{j}']=(base+u*vet).round(4).tolist()
p.write_text(json.dumps(d),encoding='utf-8')
print('PB6: projeções das forças dos apoios acrescentadas')

p=U/'threejs/pedidos3d/PB5.json';d=json.loads(p.read_text(encoding='utf-8'))
inicio=round((a['B5-5']['ini']-a['B5-1']['ini'])*15)
for f,e in d['cenas']['haltere_torto']:
    if f<inicio:continue
    fis=F.haltere(e['phi'],multiplicador_omega=3)
    e['omega_fisica']=float(3*F.WH);e['camera_lenta']=1/3
    for k in ['L','axial','transversal','torque','v','r']:e['pontos'][k]=fis[k].round(4).tolist()
    for k in list(e['pontos']):
        if k.startswith(('L:','Lz:','Lh:')):del e['pontos'][k]
    u=float(np.clip((f/15-inicio/15-1)/1.5,0,1));crescimento=1+.6*smooth(u)
    for nome,base,vet,esc in [('tau',np.zeros(3),'torque',.35),('Fsup',np.array([0,0,-.45]),'Fsup',.16),('Finf',np.array([0,0,-.85]),'Finf',.16)]:
        for j,t in enumerate(np.linspace(0,1,25)):e['pontos'][f'{nome}:{j}']=(base+t*esc*crescimento/9*fis[vet]).round(4).tolist()
p.write_text(json.dumps(d),encoding='utf-8')
print('PB5-5: regime 3 voltas/s, câmera 1/3 e setas limitadas a 1,6×')
