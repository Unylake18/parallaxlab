"""Alinhamento Manim × 3D: no .mov do Manim, a cauda da seta vx (violeta, grossa, horizontal) deve começar no centro da molécula acompanhada (proj 'm').
Mede, em quadros com a seta vx quase horizontal, a distância entre a cauda detectada e proj['m']. → qa/alinhamento_manim.txt"""
import json
from pathlib import Path
import av
import numpy as np
U = Path(__file__).resolve().parents[1]
import os
K1080 = os.environ.get('RES') == '1080'
proj = json.load(open(U / ('proj_1080x1920.json' if K1080 else 'proj.json')))
mov = U / ('media_final30/videos/cena/1920p30/GasIdeal033.mov' if K1080 else 'media_preview/videos/cena/960p15/GasIdeal033.mov')
KE = 2 if K1080 else 1
alvo = {int(q) * 2 for q in range(240, 900, 30)} if K1080 else {int(q) for q in range(240, 900, 30)}
res = []
with av.open(str(mov)) as c:
    for i, f in enumerate(c.decode(video=0)):
        if i not in alvo:
            continue
        a = f.to_ndarray(format='rgba').astype(int)
        m = (abs(a[..., 0] - 156) < 14) & (abs(a[..., 1] - 140) < 14) & (a[..., 2] > 235) & (a[..., 3] > 250)
        ys, xs = np.nonzero(m)
        p = proj[str(i)]
        if len(xs) < 60:
            continue
        # linha mais espessa da seta vx: faixa de linhas com mais pixels violeta; cauda = extremo do lado da molécula
        near = np.hypot(xs - p['m'][0], ys - p['m'][1]) < 90 * KE
        if near.sum() < 40:
            continue
        xs, ys = xs[near], ys[near]
        tip = p['tx']
        dirx = np.sign(tip[0] - p['m'][0]) or 1
        xt = xs.min() if dirx > 0 else xs.max()
        yt = ys[np.abs(xs - xt) < 3].mean()
        res.append((i, float(np.hypot(xt + (.5 if dirx > 0 else .5) - p['m'][0], yt + .5 - p['m'][1]))))
txt = f'quadros: {len(res)}; erro máx. {max(e for _, e in res):.2f} px; médio {np.mean([e for _, e in res]):.2f} px\n' + '\n'.join(f'  q{i}: {e:.2f}' for i, e in res)
(U / 'qa/alinhamento_manim.txt').write_text(txt + '\n', encoding='utf-8'); print(txt)
