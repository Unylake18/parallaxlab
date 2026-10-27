"""QA da faixa reservada à legenda (só QA; nada disso entra no vídeo).

1. Prancha: um quadro do meio de cada beat do preview, com o retângulo de teste em y_px 760–840 (540×960) e um texto de
   exemplo em Inter 23 px, base em ~835 px, para conferir num rascunho do Reels.
2. Medição: na camada do Manim (.mov com alfa), procura pixels desenhados em y_px ≥ 760 (faixa + área abaixo) em todos
   os quadros e informa os piores. No 3D, mede o brilho máximo da faixa fora das estrelas (pontos isolados).
Uso (na raiz do repositório): uv run python videos/vid_0029_campo_toroide/qa/faixa_legenda.py [--sufixo v3]
"""
import argparse
import json
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parents[1]
ROOT = UNIT.parents[1]
Y0, Y1 = 760, 840


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sufixo', default='v3')
    a = ap.parse_args()
    tl = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
    fps = 15
    want = {round((b['inicio_s'] + b['fim_s']) / 2 * fps): b['id'] for b in tl['beats']}
    frames = {}
    with av.open(str(UNIT / 'renders' / f'preview_{a.sufixo}_540x960.mp4')) as c:
        for i, f in enumerate(c.decode(video=0)):
            if i in want:
                frames[want[i]] = f.to_image()
            if len(frames) == len(want):
                break
    font = ImageFont.truetype(str(ROOT / 'assets' / 'fonts' / 'inter' / 'Inter-SemiBold.ttf'), 23)
    sheet = Image.new('RGB', (540 * 5, 960 * 2))
    for k, bid in enumerate(sorted(frames)):
        im = frames[bid].copy()
        d = ImageDraw.Draw(im, 'RGBA')
        d.rectangle([0, Y0, 539, Y1], outline=(255, 210, 0, 255), width=2, fill=(255, 210, 0, 28))
        msg = 'o campo fica preso dentro do enrolamento'
        w = d.textlength(msg, font=font)
        d.text(((540 - w) / 2, 835 - 23), msg, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        d.text((8, 8 + 20), bid, fill=(255, 210, 0, 255))
        sheet.paste(im, ((k % 5) * 540, (k // 5) * 960))
    out = UNIT / 'qa' / f'prancha_faixa_legenda_{a.sufixo}.png'
    sheet.resize((540 * 5 // 2, 960)).save(out)

    worst, n_bad = [], 0
    with av.open(str(UNIT / 'media_preview' / 'videos' / 'cena' / '960p15' / 'CampoToroide029.mov')) as c:
        for i, f in enumerate(c.decode(video=0)):
            alpha = f.to_ndarray(format='rgba')[Y0:, :, 3]
            m = int(alpha.max())
            if m > 8:
                n_bad += 1
                worst.append((m, i))
    worst.sort(reverse=True)
    lum = 0
    for i in range(0, round(tl['duracao_s'] * fps), 15):
        p = UNIT / 'frames3d_540x960' / f'f{i:05d}.png'
        g = np.asarray(Image.open(p).convert('L'), dtype=float)[Y0:Y1]
        # estrelas são pontos isolados: um filtro de mínimo 3×3 as apaga e deixa só regiões maiores
        sub = np.minimum.reduce([np.roll(np.roll(g, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
        lum = max(lum, int(sub.max()))
    print(json.dumps({'prancha': str(out.relative_to(ROOT)), 'quadros_manim_com_pixel_na_faixa_ou_abaixo': n_bad,
                      'piores_(alfa,quadro)': worst[:5], 'brilho_max_3d_na_faixa_sem_estrelas': lum}, ensure_ascii=False))


if __name__ == '__main__':
    main()
