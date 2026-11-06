"""Composição do vid_0033: 3D (PNG opaco, fundo) + Manim (.mov com alfa, por cima) → H.264.

Gera, numa passada só, renders/parte3d[_SUFIXO]_WxH.mp4 (o 3D sozinho) e renders/preview[_SUFIXO]_WxH.mp4 (composto).
Sem ffmpeg de linha de comando: usa o PyAV da .venv. CRF 14 (padrão do AGENTS.md para encoders próprios).
Uso (na raiz do repositório): uv run python videos/vid_0033_halo_22/compor.py [--res 540x960] [--fps 15] [--sufixo v2]
"""
import argparse
import json
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
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
    ap.add_argument('--midia', default='media_preview', help='pasta(s) de mídia do Manim; várias separadas por vírgula = faixas de animações em ordem (final: media_f0,...,media_f5)')
    ap.add_argument('--faixa', type=int, default=None, help='compõe só a faixa N (media_fN) -> renders/seg_N.mp4; juntar com qa/juntar.py')
    ap.add_argument('--pad', type=int, default=0, help='com --faixa: repete o último quadro do Manim N vezes (espera final estática que o Manim gravou curta)')
    ap.add_argument('--sem3d', action='store_true', help='não grava parte3d_*.mp4')
    a = ap.parse_args()
    w, h = map(int, a.res.split('x'))
    total = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))['nq']
    ini, fim = 0, total
    frames3d = UNIT / f'frames3d_{w}x{h}'
    movs = [UNIT / m / 'videos' / 'cena' / f'{h}p{a.fps}' / 'GasIdeal033.mov' for m in a.midia.split(',')]
    if a.faixa is not None:
        cont = []
        for mv in movs:
            with av.open(str(mv)) as m:
                cont.append(m.streams.video[0].frames)
        ini, fim = sum(cont[:a.faixa]), sum(cont[:a.faixa + 1])
        movs = [movs[a.faixa]]
        ini_f, fim_f = ini, fim
        fim += a.pad
    (UNIT / 'renders').mkdir(exist_ok=True)
    suf = f'_{a.sufixo}' if a.sufixo else ''
    out3d, s3d = (None, None) if a.sem3d else encoder(UNIT / 'renders' / f'parte3d{suf}_{w}x{h}.mp4', w, h, a.fps)
    outc, sc = encoder(UNIT / 'renders' / (f'seg_{a.faixa}.mp4' if a.faixa is not None else f'preview{suf}_{w}x{h}.mp4'), w, h, a.fps)

    t0 = time.time()
    def camadas():
        for mv in movs:
            with av.open(str(mv)) as m:
                for f in m.decode(video=0):
                    yield f.to_ndarray(format='rgba')
    layer = camadas()
    last = np.zeros((h, w, 4), np.uint8)
    n_manim = 0
    ex = ThreadPoolExecutor(6)                      # lê os PNG do 3D em paralelo (o gargalo era a decodificação, uma por vez)
    carga = lambda k: np.asarray(Image.open(frames3d / f'f{k:05d}.png').convert('RGB'))
    fila = deque(ex.submit(carga, k) for k in range(ini, min(ini + 24, fim)))
    for i in range(ini, fim):
        bg = fila.popleft().result()
        if i + 24 < fim:
            fila.append(ex.submit(carga, i + 24))
        fg = next(layer, None)
        if fg is None:
            fg = last
        else:
            n_manim += 1
            last = fg
        alpha = fg[..., 3:4].astype(np.float32) / 255
        # O .mov do Manim (qtrle/argb) traz alfa direto (não pré-multiplicado): over = fg·α + bg·(1 − α).
        comp = (fg[..., :3] * alpha + bg * (1 - alpha) + .5).astype(np.uint8)
        if out3d:
            write(out3d, s3d, bg)
        write(outc, sc, comp)
    for out, s in ((out3d, s3d), (outc, sc)):
        if out is None:
            continue
        for packet in s.encode():
            out.mux(packet)
        out.close()
    extra = sum(1 for _ in layer)
    info = {'quadros': total, 'quadros_manim': n_manim + extra, 'segundos': round(time.time() - t0, 1)}
    print(json.dumps(info))
    if n_manim != fim - ini - a.pad or extra:
        raise SystemExit(f'ERRO: Manim tem {n_manim + extra} quadros; esperado {fim - ini}.')


if __name__ == '__main__':
    main()
