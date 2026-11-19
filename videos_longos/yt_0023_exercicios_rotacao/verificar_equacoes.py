"""Compila todas as expressões aprovadas e mede a largura; não aprova QA visual."""
import json
from visual23 import Q,AQUI
from conteudo import CONTAS

resultados=[]
for ancora,seq in CONTAS.items():
    for cue,tex in seq:
        try:
            m=Q(tex.lstrip('!'),46,ancora.startswith('E4'))
            resultados.append(dict(ancora=ancora,tex=tex,largura=round(m.width,3),altura=round(m.height,3),compilou=True))
        except Exception as e:
            resultados.append(dict(ancora=ancora,tex=tex,compilou=False,erro=str(e)))
    print(ancora,flush=True)
(AQUI/'renders'/'compilacao_equacoes.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',len(resultados),'ERROS',sum(not r['compilou'] for r in resultados),'LARGAS',sum(r.get('largura',0)>6.1 for r in resultados),flush=True)
