"""Preflight barato das fórmulas na largura da CONTA, antes de renderizar."""
import json
from pathlib import Path
import latex25
from pecas25 import Mx
from conteudo25 import CONTAS
out=[]
for a,ss in CONTAS.items():
    for i,s in enumerate(ss):
        m,_=Mx(s,size=52 if i==len(ss)-1 else 46)
        if m.width>6.5:out.append(dict(ancora=a,indice=i,largura=m.width,tex=s))
Path('qa/formulas_largas.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
for x in out:print(x)
