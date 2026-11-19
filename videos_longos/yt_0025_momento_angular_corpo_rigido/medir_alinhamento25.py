"""Centroides verdes no PNG renderizado × projeção Manim (não usa o número devolvido pelo browser)."""
import json
import numpy as np
from PIL import Image
from pathlib import Path
U=Path(__file__).resolve().parent
casos=json.loads((U/'qa/calibracao_entrada.json').read_text(encoding='utf-8'))
out=[]
for c in casos:
    im=np.array(Image.open(U/f'qa/alinhamento/{c["nome"]}.png').convert('RGB'))
    verde=(im[:,:,1]>175)&(im[:,:,0]<70)&(im[:,:,2]<70)
    yy,xx=np.where(verde)
    for i,(x,y) in enumerate(c['esperado']):
        hit=(abs(xx-x)<9)&(abs(yy-y)<9)
        med=[float(xx[hit].mean())+.5,float(yy[hit].mean())+.5] if hit.any() else [float('inf'),float('inf')]
        erro=float(np.linalg.norm(np.array(med)-[x,y]))
        out.append(dict(quadro=c['nome'],ponto=i,esperado=[x,y],medido=med,erro_px=erro,ok=erro<=2))
(U/'qa/alinhamento.json').write_text(json.dumps(out,indent=1),encoding='utf-8')
print(len(out),'pontos,',len(casos),'quadros; erro máximo:',max(x['erro_px'] for x in out),'px; falhas:',sum(not x['ok'] for x in out))
raise SystemExit(0 if all(x['ok'] for x in out) else 1)
