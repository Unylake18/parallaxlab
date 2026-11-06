"""Confinamento das moléculas (v2): (1) numérico — todos os quadros e moléculas, inclusive o pistão do C07: o centro fica em
[−1, −1 + Lx] × [−1, 1]² e a esfera (raio r) nunca ultrapassa a parede desenhada (±(1 + r), pistão em −1 + Lx + r);
(2) em tela — o centro projetado de cada esfera fica dentro do fecho convexo dos 8 cantos projetados do recipiente
(render3d.js --audit 1 --semfoto --quadros ...; qa/proj_auditoria.json). → qa/confinamento.txt
Uso (raiz): uv run python videos/vid_0033_pvnrt/qa/confinamento.py"""
import json
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parents[1]
TL = json.loads((U / 'timeline.json').read_text(encoding='utf-8'))
R = TL['r_esf']
s0, sp = np.array(TL['s0']), np.array(TL['sp'])
tau, Lx, Gx = np.array(TL['tau']), np.array(TL['Lx']), np.array(TL['Gx'])
tri = lambda s: 2. - np.abs(np.mod(s, 4.) - 2.)
x = -1. + Lx[None, :] * tri(s0[:, 0:1] + sp[:, 0:1] * Gx[None, :]) / 2.
y = -1. + tri(s0[:, 1:2] + sp[:, 1:2] * tau[None, :])
z = -1. + tri(s0[:, 2:3] + sp[:, 2:3] * tau[None, :])
xl, xr = -1. - R, -1. + Lx[None, :] + R
exc = [float(np.max(np.maximum(xl + R - x, 0))), float(np.max(np.maximum(x - (xr - R), 0))), float(np.max(np.maximum(np.abs(y) + R - (1 + R), 0))), float(np.max(np.maximum(np.abs(z) + R - (1 + R), 0)))]
folga = float(min(np.min((xr - R) - x), np.min(x - (xl + R)), np.min((1) - np.abs(y)), np.min(1 - np.abs(z))))
linhas = [f"numérico: {x.shape[0]} moléculas × {x.shape[1]} quadros; excesso máx. além da parede (esfera inteira): esq {exc[0]:.2e} · dir/pistão {exc[1]:.2e} · y {exc[2]:.2e} · z {exc[3]:.2e}; folga mínima do centro à parede da esfera {folga:.4f} (≥ 0)",
          f"pistão: Lx de {Lx.max():.2f} a {Lx.min():.2f}; maior |x| da esfera mais a parede móvel: {float(np.max(x + R - xr)):.4f} (≤ 0)"]
ok = max(exc) <= 1e-9 and folga >= -1e-9
linhas.append('numérico: ' + ('OK' if ok else 'FALHOU'))
pa = U / 'qa' / 'proj_auditoria.json'
if pa.exists():
    P = json.loads(pa.read_text())

    def hull(pts):
        pts = sorted(map(tuple, pts))
        def meia(ps):
            h = []
            for p in ps:
                while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                    h.pop()
                h.append(p)
            return h
        return meia(pts)[:-1] + meia(pts[::-1])[:-1]
    fora, tot, pior = 0, 0, 0.
    import sys
    sys.path.insert(0, str(U))
    import roteiro as RT
    def mix(t):
        K = RT.CAM
        for a_, b_ in zip(K, K[1:]):
            if t <= b_['t']:
                return a_['mix'] + (b_['mix'] - a_['mix']) * RT.suave((t - a_['t']) / (b_['t'] - a_['t']))
        return K[-1]['mix']
    for f, p in P.items():
        if not p.get('todas') or mix(int(f) / RT.FPS) > .02:
            continue                       # no voo do hook a câmera está dentro/atrás da caixa: os cantos projetados não valem
        H = hull(p['cA'])
        for c in p['todas']:
            tot += 1
            d = min(((H[(i + 1) % len(H)][0] - H[i][0]) * (c[1] - H[i][1]) - (H[(i + 1) % len(H)][1] - H[i][1]) * (c[0] - H[i][0])) / (np.hypot(H[(i + 1) % len(H)][0] - H[i][0], H[(i + 1) % len(H)][1] - H[i][1]) or 1) for i in range(len(H)))
            pior = min(pior, d) if d < 0 else pior
            fora += d < -.01
    linhas.append(f'em tela: {tot} centros projetados em {len(P)} quadros; fora do fecho convexo dos cantos projetados: {fora} (pior {pior:.2f} px)')
(U / 'qa' / 'confinamento.txt').write_text('\n'.join(linhas) + '\n', encoding='utf-8')
print('\n'.join(linhas))
