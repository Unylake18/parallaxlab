"""Composição do vid_0032: 3D (PNG opaco, fundo) + Manim (.mov com alfa, por cima) → H.264.

3D nos trechos do timeline (trechos_3d: gancho C01 e C05/C06); fora deles o fundo é a cor do template (o Manim
cobre o 3D com um retângulo de fundo nas trocas).
Gera renders/preview[_SUFIXO]_WxH.mp4. Sem ffmpeg de linha de comando: PyAV da .venv, CRF 14, preset medium.
Uso (na raiz do repositório): uv run python videos/vid_0032_microondas_chocolate/compor.py [--res 540x960] [--fps 15] [--sufixo v2]
(v2: --sufixo v2 → renders/preview_v2_540x960.mp4; o v1 não é sobrescrito)
"""
import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

UNIT = Path(__file__).resolve().parent
BG = np.array([0x05, 0x08, 0x16], np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--res', default='540x960')
    ap.add_argument('--fps', type=int, default=15)
    ap.add_argument('--sufixo', default='')
    ap.add_argument('--midia', default='media_preview')
    a = ap.parse_args()
    w, h = map(int, a.res.split('x'))
    TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
    total = round(TL['duracao_s'] * a.fps)
    em3d = {round(x * a.fps) + k for x, y in TL['trechos_3d'] for k in range(round((y - x) * a.fps))}
    frames3d = UNIT / f'frames3d_{w}x{h}'
    mov = UNIT / a.midia / 'videos' / 'cena' / f'{h}p{a.fps}' / 'Microondas032.mov'
    (UNIT / 'renders').mkdir(exist_ok=True)
    suf = f'_{a.sufixo}' if a.sufixo else ''
    out = av.open(str(UNIT / 'renders' / f'preview{suf}_{w}x{h}.mp4'), 'w')
    s = out.add_stream('libx264', rate=Fraction(a.fps))
    s.width, s.height, s.pix_fmt = w, h, 'yuv420p'
    s.options = {'crf': '14', 'preset': 'medium'}

    t0 = time.time()
    manim = av.open(str(mov))
    layer = (f.to_ndarray(format='rgba') for f in manim.decode(video=0))
    last = np.zeros((h, w, 4), np.uint8)
    n_manim = 0
    fundo = np.broadcast_to(BG, (h, w, 3))
    for i in range(total):
        bg = np.asarray(Image.open(frames3d / f'f{i:05d}.png').convert('RGB'), np.float32) if i in em3d else fundo
        fg = next(layer, None)
        if fg is None:
            fg = last
        else:
            n_manim += 1
            last = fg
        alpha = fg[..., 3:4].astype(np.float32) / 255
        comp = (fg[..., :3] * alpha + bg * (1 - alpha) + .5).astype(np.uint8)   # alfa direto (qtrle/argb)
        for p in s.encode(av.VideoFrame.from_ndarray(comp, format='rgb24')):
            out.mux(p)
    for p in s.encode():
        out.mux(p)
    out.close()
    extra = sum(1 for _ in layer)
    print(json.dumps({'quadros': total, 'quadros_3d': len(em3d), 'quadros_manim': n_manim + extra, 'segundos': round(time.time() - t0, 1)}))
    if n_manim != total or extra:
        print(f'AVISO: Manim tem {n_manim + extra} quadros; o vídeo tem {total}.')


if __name__ == '__main__':
    main()
