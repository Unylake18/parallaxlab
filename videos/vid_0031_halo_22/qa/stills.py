"""Stills 1080×1920 do vid_0031 (v6 §B.11): compõe a camada Manim (RGBA) sobre o 3D nos quadros pedidos.
Passos (na raiz do repositório):
  1) uv run python videos/vid_0031_halo_22/qa/stills.py --quadros      → imprime os quadros (estados escolhidos)
  2) cd videos/vid_0031_halo_22 && node render3d.js --w 1080 --h 1920 --out qa/stills3d --quadros <lista>
  3) MIDIA=media_stills STILLS=<lista> SECO=1 uv run python -m manim -t --dry_run --disable_caching --progress_bar none
     -r 1080,1920 --fps 15 videos/vid_0031_halo_22/cena.py HaloSol031
  4) uv run python videos/vid_0031_halo_22/qa/stills.py                → qa/still_<estado>_1080x1920.png
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

QA = Path(__file__).resolve().parent
UNIT = QA.parent
ESTADOS = {'C01_cristais': 0, 'C02_lupa': 0, 'C05_oposta': 0, 'C05_vizinha': 0, 'C05_alternada_olho': 0, 'C06_b2_eq': 0,
           'C06_payoff': 0, 'C08_snell_4': 0, 'C09_cone_girando': 0, 'C10_zoom_curvas': 0, 'C11_fios': 0}      # v7 §B.9


def quadros():
    ev = {e['estado']: e['quadro'] for e in json.loads((UNIT / 'media_seco' / 'estados.json').read_text(encoding='utf-8'))['eventos']}
    return {n: ev[n] - 1 + d for n, d in ESTADOS.items()}


def main():
    q = quadros()
    if '--quadros' in sys.argv:
        print(','.join(str(v) for v in q.values()))
        return
    for n, f in q.items():
        fundo = np.asarray(Image.open(QA / 'stills3d' / f'f{f:05d}.png').convert('RGB')).astype(np.float32)
        fg = np.asarray(Image.open(UNIT / 'media_stills' / 'stills' / f'{f}.png').convert('RGBA')).astype(np.float32)
        a = fg[..., 3:4] / 255
        comp = (fg[..., :3] * a + fundo * (1 - a) + .5).astype(np.uint8)
        Image.fromarray(comp).save(QA / f'still_{n}_1080x1920.png')
        print(n, f)


if __name__ == '__main__':
    main()
