"""Alinhamento 3D × proj.json: render de depuração (só a esfera acompanhada, magenta puro) e centroide dos pixels magenta
versus a projeção 'm' do proj.json. Uso: node render3d.js --debug 1 --quadros <lista>; depois este script. → qa/alinhamento.txt"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

UNIT = Path(__file__).resolve().parents[1]
D = UNIT / 'qa' / 'debug_540x960'
proj = json.loads((D / 'proj.json').read_text())
erros = []
for f, p in proj.items():
    a = np.asarray(Image.open(D / f'f{int(f):05d}.png').convert('RGB')).astype(int)
    m = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)
    if m.sum() < 5:
        continue                                   # esfera fora da tela/atrás de nada: ignora
    ys, xs = np.nonzero(m)
    erros.append((int(f), float(np.hypot(xs.mean() + .5 - p['m'][0], ys.mean() + .5 - p['m'][1]))))
txt = f'quadros medidos: {len(erros)}; erro máximo {max(e for _, e in erros):.2f} px; médio {np.mean([e for _, e in erros]):.2f} px\n' + '\n'.join(f'  q{f}: {e:.2f} px' for f, e in erros)
(UNIT / 'qa' / 'alinhamento.txt').write_text(txt + '\n', encoding='utf-8')
print(txt)
