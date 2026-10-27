"""Composição do vid_0029: 3D (PNG opaco, fundo) + Manim (.mov com alfa, por cima) → H.264.

Gera, numa passada só, renders/parte3d[_SUFIXO]_WxH.mp4 (o 3D sozinho) e renders/preview[_SUFIXO]_WxH.mp4 (composto).
Sem ffmpeg de linha de comando: usa o PyAV da .venv. CRF 14 (padrão do AGENTS.md para encoders próprios).
Uso (na raiz do repositório): uv run python videos/vid_0029_campo_toroide/compor.py [--res 540x960] [--fps 15] [--sufixo v2]
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


def encoder(path, w, h, fps):
    out = av.open(str(path), 'w')
    s = out.add_stream('libx264', rate=Fraction(fps))
    s.width, s.height, s.pix_fmt = w, h, 'yuv420p'
    s.options = {'crf': '14', 'preset': 'medium'}
    return out, s


def write(out, stream, rgb):
    for packet in stream.encode(av.VideoFrame.from_ndarray(rgb, format='rgb24')):
        out.mux(packet)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--res', default='540x960')
    ap.add_argument('--fps', type=int, default=15)
    ap.add_argument('--sufixo', default='', help='ex.: v2 → preview_v2_540x960.mp4 (preserva versões anteriores)')
    ap.add_argument('--midia', default='media_preview', help='pasta de mídia do Manim (final: media_final)')
    a = ap.parse_args()
    w, h = map(int, a.res.split('x'))
    total = round(json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))['duracao_s'] * a.fps)
    frames3d = UNIT / f'frames3d_{w}x{h}'
    mov = UNIT / a.midia / 'videos' / 'cena' / f'{h}p{a.fps}' / 'CampoToroide029.mov'
    (UNIT / 'renders').mkdir(exist_ok=True)
    suf = f'_{a.sufixo}' if a.sufixo else ''
    out3d, s3d = encoder(UNIT / 'renders' / f'parte3d{suf}_{w}x{h}.mp4', w, h, a.fps)
    outc, sc = encoder(UNIT / 'renders' / f'preview{suf}_{w}x{h}.mp4', w, h, a.fps)

    t0 = time.time()
    manim = av.open(str(mov))
    layer = (f.to_ndarray(format='rgba') for f in manim.decode(video=0))
    last = np.zeros((h, w, 4), np.uint8)
    n_manim = 0
    for i in range(total):
        bg = np.asarray(Image.open(frames3d / f'f{i:05d}.png').convert('RGB'))
        fg = next(layer, None)
        if fg is None:
            fg = last
        else:
            n_manim += 1
            last = fg
        alpha = fg[..., 3:4].astype(np.float32) / 255
        # O .mov do Manim (qtrle/argb) traz alfa direto (não pré-multiplicado): over = fg·α + bg·(1 − α).
        comp = (fg[..., :3] * alpha + bg * (1 - alpha) + .5).astype(np.uint8)
        write(out3d, s3d, bg)
        write(outc, sc, comp)
    for out, s in ((out3d, s3d), (outc, sc)):
        for packet in s.encode():
            out.mux(packet)
        out.close()
    extra = sum(1 for _ in layer)
    info = {'quadros': total, 'quadros_manim': n_manim + extra, 'segundos': round(time.time() - t0, 1)}
    print(json.dumps(info))
    if n_manim != total or extra:
        print(f'AVISO: Manim tem {n_manim + extra} quadros; o 3D tem {total}.')


if __name__ == '__main__':
    main()
