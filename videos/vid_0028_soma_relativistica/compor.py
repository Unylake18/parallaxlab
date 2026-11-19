"""Composição: 3D (PNGs opacos, fundo) + Manim (.mov com alfa, por cima) → H.264.

Gera numa passada renders/parte3d[_SUFIXO]_WxH.mp4 (só o 3D) e renders/preview[_SUFIXO]_WxH.mp4 (composto).
Usa o PyAV da .venv (sem ffmpeg de linha de comando). CRF 14, o padrão do AGENTS.md para encoders próprios.
Uso (na raiz do repositório):
  uv run python videos/vid_NNNN_x/compor.py --classe MinhaCena [--res 540x960] [--fps 15] [--sufixo v2]
O .mov é procurado em <unidade>/media_preview/videos/cena/<H>p<FPS>/<Classe>.mov (render do Manim com -t e
MEDIA_DIR=<unidade>/media_preview); --mov aponta outro caminho.
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


def retangulo(s, x0, y0, largura):
    """Retângulo (em px, 1 px de folga) de uma imagem 2172 × 724 de largura `largura`, canto sup. esq. em (x0, y0) unidades do topo/esq."""
    return (slice(max(int(y0 * s) - 1, 0), int((y0 + largura * 724 / 2172) * s) + 2),
            slice(max(int(x0 * s) - 1, 0), int((x0 + largura) * s) + 2))


def fundo_k(mov):
    """K = cor guardada nos pixels com α = 0 do 1º quadro do .mov (o background_color da cena; preto se a cena não o define)."""
    with av.open(str(mov)) as c:
        q = next(c.decode(video=0)).to_ndarray(format='rgba')
    return np.median(q[q[..., 3] == 0][:, :3], axis=0).astype(np.float32)


def sobrepor(comp, fg, logos, K):
    """over do .mov do Manim sobre comp (float32 RGB).

    O .mov do Manim (qtrle/argb, -t) NÃO é alfa direto (medido no vid_0029): o quadro vazio guarda K com α = 0 e o Cairo
    desenha por cima em pré-multiplicado, então vetores e textos saem como cor·α + K·(1 − α). Aqui a cena não define
    background_color: K = (0, 0, 0) medido, ou seja, pré-multiplicado puro (cor·α).
    over correto: rgb + (comp − K)·(1 − α). Tratar como alfa direto (rgb·α) escurecia bordas e translúcidos (α²).
    Exceção: ImageMobject (só os logos) entra em alfa direto (rgb = cor) → over clássico nos retângulos dos logos.
    """
    alpha = fg[..., 3:4].astype(np.float32) / 255
    rgb = fg[..., :3].astype(np.float32)
    out = rgb + (comp - K) * (1 - alpha)
    for ly, lx in logos:
        out[ly, lx] = rgb[ly, lx] * alpha[ly, lx] + comp[ly, lx] * (1 - alpha[ly, lx])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--classe', required=True, help='classe da cena Manim (nome do .mov)')
    ap.add_argument('--res', default='540x960')
    ap.add_argument('--fps', type=int, default=15)
    ap.add_argument('--sufixo', default='', help='ex.: v2 → preview_v2_540x960.mp4 (preserva versões anteriores)')
    ap.add_argument('--mov', type=Path, help='caminho do .mov do Manim, se não estiver no lugar padrão')
    a = ap.parse_args()
    w, h = map(int, a.res.split('x'))
    total = round(json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))['duracao_s'] * a.fps)
    frames3d = UNIT / f'frames3d_{w}x{h}'
    mov = a.mov or UNIT / 'media_preview' / 'videos' / 'cena' / f'{h}p{a.fps}' / f'{a.classe}.mov'
    (UNIT / 'renders').mkdir(exist_ok=True)
    suf = f'_{a.sufixo}' if a.sufixo else ''
    out3d, s3d = encoder(UNIT / 'renders' / f'parte3d{suf}_{w}x{h}.mp4', w, h, a.fps)
    outc, sc = encoder(UNIT / 'renders' / f'preview{suf}_{w}x{h}.mp4', w, h, a.fps)

    tl = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
    s = w / 9  # px por unidade (quadro 9 × 16)
    marca = retangulo(s, 9 - .25 - 1.8, .25, 1.8)  # marca d'água: largura 1,8, to_corner(UR, buff=.25), o vídeo todo
    cta = retangulo(s, 4.5 - 2.3, 8 - 2.4 - 4.6 / 6, 4.6)  # logo do CTA: largura 4,6 em (0, 2,4), só a partir de 'cta'
    q_cta = round(tl['eventos']['cta'] * a.fps)
    K = fundo_k(mov)
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
        comp = sobrepor(bg.astype(np.float32), fg, [marca, cta] if i >= q_cta else [marca], K)
        comp = np.clip(comp + .5, 0, 255).astype(np.uint8)
        write(out3d, s3d, bg)
        write(outc, sc, comp)
    for out, s in ((out3d, s3d), (outc, sc)):
        for packet in s.encode():
            out.mux(packet)
        out.close()
    extra = sum(1 for _ in layer)
    print(json.dumps({'quadros': total, 'quadros_manim': n_manim + extra, 'segundos': round(time.time() - t0, 1)}))
    if n_manim != total or extra:
        print(f'AVISO: o Manim tem {n_manim + extra} quadros; o 3D tem {total}. Confira o timeline e os waits do cena.py.')


if __name__ == '__main__':
    main()
