"""Calcula/refina escalas.json (fator de velocidade de cada trecho entre âncoras).
Passo 1 (MEDIR=1 -> medicao.json): k = (janela da voz - folga) / duração natural, limitado a [KMIN, 1].
Passos seguintes (render/dry-run normal -> chegada.json): reduz k dos trechos que chegaram atrasados à próxima âncora."""
import json, sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
A = json.loads((PASTA / 'ancoras.json').read_text(encoding='utf-8'))['A']
KMIN, FOLGA = 0.30, 0.10
esc_p = PASTA / 'escalas.json'
modo = sys.argv[1] if len(sys.argv) > 1 else 'medicao'
if modo == 'medicao':
    d = json.loads((PASTA / 'medicao.json').read_text(encoding='utf-8'))
    ordem, arr = d['order'], d['arr']
    esc = {}
    for cur, nxt in zip(ordem, ordem[1:]):
        need, nat = A[nxt] - A[cur], arr[nxt] - arr[cur]
        esc[cur] = round(max(KMIN, min(1.0, (need - FOLGA) / nat)) if nat > 0 else 1.0, 3)
    esc[ordem[-1]] = 1.0
    for n in ordem[:-1]:
        pass
else:
    d = json.loads((PASTA / 'chegada.json').read_text(encoding='utf-8'))
    ordem, arr = d['order'], d['arr']
    esc = json.loads(esc_p.read_text(encoding='utf-8'))
    pior = 0
    for cur, nxt in zip(ordem, ordem[1:]):
        atraso = arr[nxt] - A[nxt]
        pior = max(pior, atraso)
        if atraso > 0.06:
            ini = max(A[cur], arr[cur]); dur = arr[nxt] - ini; need = A[nxt] - ini
            esc[cur] = round(max(KMIN, esc.get(cur, 1.0) * max(0.5, (need - FOLGA) / dur)), 3)
    print('pior atraso (s):', round(pior, 3))
esc_p.write_text(json.dumps(esc, indent=1), encoding='utf-8')
apertados = {k: v for k, v in esc.items() if v < 0.6}
print('trechos com k<0,6 (muito comprimidos):', apertados)
if modo != 'medicao':
    tarde = [(n, round(arr[n] - A[n], 2)) for n in ordem if arr[n] - A[n] > 0.06]
    print('atrasados:', tarde)
