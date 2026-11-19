"""Pontos de teste de projeção (modelos físicos), independentes da API do browser."""
import json
from pathlib import Path
import numpy as np
import latex25
from pecas25 import CAMS,proj,px,ESC_V
import fisica25 as F
U=Path(__file__).resolve().parent
(U/'threejs/cameras25.json').write_text(json.dumps(CAMS),encoding='utf-8')
casos=[]
for nome,tipo,cam,fn,esc in [('p','pendulo_conico','P_34',F.pendulo,1.6),('v','corpo_voxel','V_34',F.voxel,ESC_V),('h','haltere_torto','H_34',F.haltere,1.8),('r','roda_balanceamento','R_34',F.roda,2.1)]:
    for k,phi in enumerate(np.linspace(0,2*np.pi,6,endpoint=False)):
        camera='H_LADO' if nome=='h' and k==5 else cam
        if camera=='H_LADO':phi=0
        e=fn(phi);ps=[e['O'].tolist(),e['massa'].tolist(),(esc*e['L']).tolist()]
        estado=dict(tipo=tipo,cam=CAMS[camera],phi=phi,pontos={},rotacao=e.get('rotacao',np.eye(3)).tolist())
        casos.append(dict(nome=f'{nome}{k}',estado=estado,pontos=ps,esperado=[px(proj(CAMS[camera],p)) for p in ps]))
# v4: todas as câmeras novas/planos (CLOSE, TOPO, AXIAL, MANCAL, hook ortográfico, plataforma), 3 pontos de mundo × 2 fases por câmera
TIPO_CAM={'P_CLOSE':'pendulo_conico','V_CLOSE':'corpo_voxel','H_TOPO':'haltere_torto','H_MANCAL':'haltere_torto','H_LADO':'haltere_torto','R_CLOSE':'roda_balanceamento','R_AXIAL':'roda_balanceamento','D_34':'bancada_dupla','D_S1':'bancada_dupla','H_34':'haltere_torto','PL_34':'plataforma_livre','PL_TOPO':'plataforma_livre'}
for nome,tipo in TIPO_CAM.items():
    for k,phi in enumerate((0.,1.1)):
        ps=[[0,0,0],[.15,.1,.2],[-.2,.1,.3]]
        estado=dict(tipo=tipo,cam=CAMS[nome],phi=phi,pontos={},rotacao=np.eye(3).tolist(),tilt=0,raio_m=.4)
        casos.append(dict(nome=f'{nome}_{k}',estado=estado,pontos=ps,esperado=[px(proj(CAMS[nome],np.array(p,float))) for p in ps]))
(U/'qa/calibracao_entrada.json').write_text(json.dumps(casos),encoding='utf-8')
