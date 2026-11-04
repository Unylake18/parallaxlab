"""Quadros rápidos (540x960, só o Manim sobre fundo escuro) dos estados pedidos: uso  mini_stills.py ESTADO1 ESTADO2 ...  → qa/teste3d_v7/mini.png"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
UNIT = Path(__file__).resolve().parents[1]
ev = {e['estado']: e['quadro'] for e in json.loads((UNIT / 'media_seco' / 'estados.json').read_text(encoding='utf-8'))['eventos']}
est = sys.argv[1:]
qs = [ev[n] - 1 for n in est]
env = dict(os.environ, SECO='1', MIDIA='media_mini', STILLS=','.join(map(str, qs)))
subprocess.run([sys.executable, '-m', 'manim', '-t', '--disable_caching', '-r', '540,960', '--fps', '15', str(UNIT / 'cena.py'), 'HaloSol031',
                '--dry_run', '--progress_bar', 'none'], env=env, cwd=UNIT.parents[1], capture_output=True)
W = 540
m = Image.new('RGB', (W * len(qs), 960), (5, 8, 22))
for i, q in enumerate(qs):
    fg = Image.open(UNIT / 'media_mini' / 'stills' / f'{q}.png').convert('RGBA')
    bg = Image.new('RGBA', fg.size, (5, 8, 22, 255)); bg.alpha_composite(fg)
    m.paste(bg.convert('RGB'), (i * W, 0))
m.save(UNIT / 'qa' / 'teste3d_v7' / 'mini.png'); print('ok', est)
