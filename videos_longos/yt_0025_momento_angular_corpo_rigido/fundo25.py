"""Rastreia estrelas no raster do preview, inclusive entre os lotes."""
from pathlib import Path
import json
import av
import numpy as np
from scipy.ndimage import gaussian_filter,label,center_of_mass,sum_labels
U=Path(__file__).resolve().parent
def estrelas(rgb):
    # Faixa sem cabeçalho nem fórmulas; ignora manchas grandes e usa só pontos isolados.
    g=rgb[73:113,24:936].astype(float).mean(2)
    g=np.maximum(0,g-gaussian_filter(g,2.0));lab,n=label(g>10)
    if not n:return np.empty((0,2))
    areas=sum_labels(np.ones_like(g),lab,range(1,n+1));centros=np.array(center_of_mass(g,lab,range(1,n+1)))
    return centros[(areas>=2)&(areas<45)]
c=av.open(str(U/'renders/preview_yt0025_v1_960x540.mp4'));ant=None;medidas=[]
for i,f in enumerate(c.decode(video=0)):
    ps=estrelas(f.to_ndarray(format='rgb24'));dx=[]
    if ant is not None and len(ant) and len(ps):
        delta=ps[:,None,:]-ant[None,:,:];custo=delta[:,:,1]**2+9*delta[:,:,0]**2
        pares=sorted((custo[j,k],j,k) for j,k in zip(*np.where((abs(delta[:,:,0])<1.8)&(abs(delta[:,:,1])<8))))
        usados_a=set();usados_b=set()
        for _,j,k in pares:
            if j in usados_a or k in usados_b:continue
            usados_a.add(j);usados_b.add(k);dx.append(float(delta[j,k,1]))
        medidas.append(dict(quadro=i,pares=len(dx),dx_mediano=float(np.median(dx)) if dx else None))
    ant=ps
c.close()
avaliados=[x for x in medidas if x['pares']>=4];suspeitos=[x for x in avaliados if x['dx_mediano']>=-.15]
off=json.loads((U/'offsets.json').read_text(encoding='utf-8'));emendas={l:[x for x in medidas if abs(x['quadro']-round(t*15))<=2] for l,t in off.items() if t>0}
out=dict(metodo='Centroides de estrelas isoladas na faixa y=73..113 px; pareamento único por proximidade, sem impor direção.',quadros_avaliados=len(avaliados),suspeitos=suspeitos,emendas=emendas)
(U/'qa/fundo.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
np.save(U/'qa/fundo_dx.npy',np.array([[x['quadro'],x['pares'],x['dx_mediano'] or 0] for x in medidas]))
print(f'{len(avaliados)} quadros avaliados; {len(suspeitos)} candidatos sem deslocamento à esquerda; inspeção exigida se houver.')
