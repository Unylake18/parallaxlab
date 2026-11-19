"""Confere, por lote, se cada trecho entre marcas cabe na voz (A animação + W espera vs D da voz): escala mínima exigida do plano()."""
import json, re, sys
LEAD = 0.09
anc = json.load(open('ancoras.json', encoding='utf-8'))['ancoras']
def kfrase(aid, fr):
    fala = anc[aid]['fala'].split(); alvo = re.findall(r'\w+', fr.lower())
    return next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
def tgt(kid):
    ps = kid.split(':', 2)
    if len(ps) < 2 or ps[1] not in anc: return None
    kind, aid, arg = ps[0], ps[1], (ps[2] if len(ps) > 2 else '')
    a = anc[aid]
    if kind == 'an': return a['ini']
    if kind == 'gat':
        k = kfrase(aid, arg)
        return None if k is None else a['ini'] + max(0.0, a['t'][k] - LEAD)
    tw, nom = a['t'], a['nominal']
    import numpy as np
    xs = [0.0] + [0.15 + k / 2.7 for k in range(len(tw))] + [max(nom, 0.15 + len(tw) / 2.7)]
    ys = [0.0] + list(tw) + [a['dur']]
    return a['ini'] + max(0.0, float(np.interp(float(arg) * nom, xs, ys)) - LEAD)
def plano(A, W, D):
    if A + W < 1e-6: return 1.0, 1.0
    if D >= A + W:
        s_ = min(1.8, max(1.0, (D / (A + W)) ** 0.5)); return s_, (max(1.0, (D - s_ * A) / W) if W > 1e-6 else 1.0)
    wp = max(0.15 * W, D - A)
    if A + wp <= D + 1e-6: return 1.0, wp / W if W > 1e-6 else 1.0
    return max(0.5, (D - wp) / A), (wp / W if W > 1e-6 else 1.0)
tot_over = 0
for L in sys.argv[1:]:
    m = json.load(open(f'medicao_{L}.json', encoding='utf-8'))['marcas']
    print(f'== {L}: {len(m)} marcas')
    # cada marca i guarda A/W do trecho que COMEÇA nela até a marca seguinte
    for i in range(len(m) - 1):
        t0, t1 = tgt(m[i]['id']), tgt(m[i + 1]['id'])
        if t0 is None or t1 is None: continue
        D = t1 - t0; A, W = m[i]['A'], m[i]['W']
        s, w = plano(A, W, D)
        if s <= 0.8 or D < A * 0.5:
            falta = max(0.0, A * 0.5 + 0.15 * W - D) if s <= 0.5 + 1e-9 else 0.0
            print(f'  {m[i]["id"][:70]:70s} A={A:5.2f} W={W:5.2f} D={D:5.2f} escala={s:.2f}' + (f'  ESTOURO {falta:.2f}s' if falta else ''))
            tot_over += falta
print('estouro total (s):', round(tot_over, 2))
