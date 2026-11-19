"""ÂNGULO NA TELA (handoff v3 §4.3): por âncora e vetor, o vetor dito ⟂ ao eixo precisa ler 60–120° (perfil) ou 90° ± 5° (axial) em ao menos um plano mantido por >= 2 s.
uso: python angulo_tela25.py [LOTE=PB6]  → qa/angulo_tela_LOTE.txt"""
import re,sys,json
from pathlib import Path
U=Path(__file__).resolve().parent
lote=sys.argv[1] if len(sys.argv)>1 else 'PB6'
log=(U/f'log_aud_{lote}.txt').read_text(encoding='utf-8',errors='replace')
tempos=json.loads((U/f'tempos_{lote}.json').read_text(encoding='utf-8'))['inicios']
ids=list(tempos);ts=[tempos[k] for k in ids]+[1e9]
amostras={}
for m in re.finditer(r'\[audit\]\s+([\d.]+)s ANGULO TELA (\w+) (PERFIL|AXIAL) ([\d.-]+)( FALHA)?',log):
    t=float(m.group(1));k=next(i for i in range(len(ids)) if ts[i]<=t<ts[i+1])
    amostras.setdefault((ids[k],m.group(2)),[]).append((t,m.group(3),float(m.group(4)),not m.group(5)))
out=[];falha=0
for (aid,vet),v in sorted(amostras.items()):
    v.sort();melhor=0;seq=0;ult=None
    for t,pl,a,ok in v:
        if ok and (ult is not None and t-ult<=1.01 and seq>0):seq+=1
        elif ok:seq=1
        else:seq=0
        ult=t;melhor=max(melhor,seq)
    passa=melhor>=2;falha+=0 if passa else 1
    out.append(f'  {aid} {vet}: {len(v)} amostras, maior sequência OK {melhor} s'+('' if passa else ' FALHA (< 2 s)'))
cab=f'ÂNGULO NA TELA {lote}: {len(amostras)} pares âncora×vetor, {falha} com FALHA'
(U/'qa'/f'angulo_tela_{lote}.txt').write_text('\n'.join([cab]+out),encoding='utf-8');print(cab)
