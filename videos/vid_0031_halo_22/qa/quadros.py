"""Extrai do preview composto os quadros de QA da §13 (PNG) e uma prancha com todos.
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/quadros.py [--video renders/preview_540x960.mp4]
"""
import argparse
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw

QA = Path(__file__).resolve().parent
# v2: os quadros-chave são os estados marcados com qa na própria cena (media_preview/qa_geometria.json)
ESTADOS = [(e['estado'], e['quadro'] / 15) for e in json.loads((QA.parent / 'media_preview' / 'qa_geometria.json')
                                                               .read_text(encoding='utf-8'))['estados']]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', default=str(QA.parent / 'renders' / 'preview_540x960.mp4'))
    a = ap.parse_args()
    (QA / 'quadros').mkdir(exist_ok=True)
    c = av.open(a.video)
    fps = float(c.streams.video[0].average_rate)
    alvos = {max(round(t * fps) - 1, 0): n for n, t in ESTADOS}     # último quadro do estado (antes do próximo passo)
    imgs = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in alvos:
            im = f.to_image()
            im.save(QA / 'quadros' / f'{alvos[i]}.png')
            imgs[alvos[i]] = im
    w, h = 270, 480
    cols = 8
    prancha = Image.new('RGB', (w * cols, (h + 22) * -(-len(ESTADOS) // cols)), (12, 14, 24))
    d = ImageDraw.Draw(prancha)
    for k, (n, t) in enumerate(ESTADOS):
        x, y = (k % cols) * w, (k // cols) * (h + 22)
        if n in imgs:
            prancha.paste(imgs[n].resize((w, h)), (x, y + 22))
        d.text((x + 4, y + 4), f'{n} ({t:.1f}s)', fill=(230, 230, 240))
    prancha.save(QA / 'prancha_preview_v7.png')
    print(f'{len(imgs)} quadros salvos em {QA}')


if __name__ == '__main__':
    main()
