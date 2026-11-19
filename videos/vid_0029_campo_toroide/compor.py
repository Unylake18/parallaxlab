"""Composição do vid_0029: 3D (PNG opaco, fundo) + Manim (.mov com alfa, por cima) → H.264.

Gera, numa passada só, renders/parte3d[_SUFIXO]_WxH.mp4 (o 3D sozinho) e renders/preview[_SUFIXO]_WxH.mp4 (composto).
Sem ffmpeg de linha de comando: usa o PyAV da .venv. CRF 14 (padrão do AGENTS.md para encoders próprios).
Uso (na raiz do repositório): uv run python videos/vid_0029_campo_toroide/compor.py [--res 540x960] [--fps 15] [--sufixo v2]
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).absolute().parents[2]))  # raiz do repo sem resolver o junction da unidade (→ K:)
from template.config import BACKGROUND_COLOR  # noqa: E402


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

    global K, LOGO
    K = np.array([int(BACKGROUND_COLOR[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    # logo: largura 1,8 no canto UP+RIGHT (buff 0,28) de um quadro 9 × 16 → x 830–1046, y 34–106 px em 1080 × 1920
    s = w / 9
    LOGO = (slice(int(.28 * s) - 1, int((.28 + 1.8 * 724 / 2172) * s) + 1), slice(int((9 - .28 - 1.8) * s) - 1, int((9 - .28) * s) + 1))
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
        rgb = fg[..., :3].astype(np.float32)
        # O .mov do Manim (qtrle/argb, -t) NÃO é alfa direto (medido): o quadro vazio guarda K = BACKGROUND_COLOR com α = 0 e
        # o Cairo desenha por cima em pré-multiplicado, então vetores e textos saem como cor·α + K·(1 − α).
        # over correto: rgb − K·(1 − α) + bg·(1 − α). Tratar como alfa direto (rgb·α) escurecia bordas e translúcidos (α²).
        comp = rgb + (bg - K) * (1 - alpha)
        # Exceção: ImageMobject (só o logo) entra em alfa direto (rgb = cor) → over clássico no retângulo do logo.
        ly, lx = LOGO
        comp[ly, lx] = rgb[ly, lx] * alpha[ly, lx] + bg[ly, lx] * (1 - alpha[ly, lx])
        comp = np.clip(comp + .5, 0, 255).astype(np.uint8)
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
