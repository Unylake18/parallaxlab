"""Reprojeta as mesmas poses/tempos nas câmeras corrigidas; atualiza o cubo de superfície."""
import json
import numpy as np
from pathlib import Path
import latex25
from pecas25 import CAMS,ESC_V,ESC_LI
import fisica25 as F
U=Path(__file__).resolve().parent
for p in (U/'threejs/pedidos3d').glob('*.json'):
    d=json.loads(p.read_text(encoding='utf-8'));novo=d.get('layout25',0)<2
    for tipo,lista in d['cenas'].items():
        for f,e in lista:
            if tipo=='pendulo_conico':e['cam']['fov']=CAMS['P_34']['fov']
            if tipo=='haltere_torto':
                e['cam'].update(K=CAMS['H_34']['K'],yc=CAMS['H_34']['yc'],alvo=CAMS['H_34']['alvo'])
            if tipo!='corpo_voxel':continue
            e['cam']=dict(CAMS['V_34'])
            R=np.array(e['rotacao']);ps=np.array(F.VOX['posicoes'])@R.T;r=ps[F.VOX['destaque']]
            v=np.cross(np.pi*F.Z,r);li=np.cross(r,.01*v)
            e['pontos'].update(massa=r.round(4).tolist(),r=r.round(4).tolist(),v=v.round(4).tolist())
            if novo:
                for k in list(e['pontos']):
                    if k.startswith(('L:','Lz:','Lh:')):e['pontos'][k]=(np.array(e['pontos'][k])*4/3).round(4).tolist()
            for nome,a,b in [('r',np.zeros(3),r),('rho',np.zeros(3),r*[1,1,0]),('z',r*[1,1,0],r),('v',r,r+.6*v),('Li_z',r,r+ESC_LI*li*[0,0,1]),('Li_h',r,r+ESC_LI*li*[1,1,0])]:
                if nome+':0' not in e['pontos']:continue
                for j,t in enumerate(np.linspace(0,1,25)):e['pontos'][f'{nome}:{j}']=(a+t*(b-a)).round(4).tolist()
    d['layout25']=2;p.write_text(json.dumps(d),encoding='utf-8')
print('Câmeras e cubo de superfície atualizados, sem mudar as durações')
