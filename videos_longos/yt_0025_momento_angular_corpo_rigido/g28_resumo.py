"""Resumo do G28 por lote e categoria, a partir dos [audit] dos log_aud_<L>.txt (v4). uso: python g28_resumo.py PH PB3 ...  → qa/g28_resumo.txt"""
import re,sys
from collections import Counter,defaultdict
from pathlib import Path
U=Path(__file__).resolve().parent
lotes=sys.argv[1:] or ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']
ign=('MANCAIS ANGULO','RODA ','ANGULO TELA','CHAMADA CRUZA CORPO')
out=[];tot=Counter()
for l in lotes:
    f=U/f'log_aud_{l}.txt'
    if not f.exists():continue
    c=Counter();ex={}
    for ln in f.read_text(encoding='utf-8',errors='replace').splitlines():
        m=re.match(r'\[audit\]\s+([0-9.]+)s (.*)',ln)
        if not m:continue
        r=m.group(2)
        if r.startswith(ign) and 'FALHA' not in r:continue
        cat=re.match(r'([A-ZÇÃÕÉÍÂÊÓÚ ]+?)(?= \'|\s\(|\s[a-z0-9<>]|$)',r);cat=(cat.group(1).strip() if cat else r[:24])
        c[cat]+=1;ex.setdefault(cat,(m.group(1),r[:110]))
    out.append(f'{l}: {sum(c.values())} ocorrências')
    for k,v in c.most_common():out.append(f'    {k:28s} {v:5d}   ex.: t={ex[k][0]}s {ex[k][1]}')
(U/'qa'/'g28_resumo.txt').write_text('\n'.join(out),encoding='utf-8');print('\n'.join(out))
