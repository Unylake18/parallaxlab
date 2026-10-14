"""Empacota os PNGs de preview em MP4 e folhas de inspeção; não gera master.

.venv/Scripts/python.exe experimentos/blender/arsenal/montar_previews_liquido_rotacao.py
Usa Pillow/PyAV já presentes no ambiente. Não modifica os PNGs de origem.
"""
import argparse
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent / 'previews/liquido_rotacao_rodada3'
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
FUNDO = '#050816'


def main():
    global PASTA
    ap = argparse.ArgumentParser()
    ap.add_argument('--pasta', type=Path, default=PASTA)
    PASTA = ap.parse_args().pasta.resolve()
    resumo = {}
    nomes = [('fenomeno_lambda0', 'Fenômeno: plano'), ('fenomeno_lambda1', 'Fenômeno: paraboloide'),
             ('geometria_meridiana', 'Geometria: seção meridiana')]
    sheet = Image.new('RGB', (810, 516), FUNDO)
    draw = ImageDraw.Draw(sheet)
    for i, (nome, titulo) in enumerate(nomes):
        with Image.open(PASTA / f'{nome}.png') as img:
            sheet.paste(img.convert('RGB').resize((270, 480)), (270*i, 36))
        draw.text((270*i+8, 8), titulo, font=FONT, fill='white')
    sheet.save(PASTA / 'comparacao.png')
    tipos = [tipo for tipo in ['morph', 'rotacao', 'payoff', 'loop_qa'] if (PASTA / tipo).is_dir()]
    film = Image.new('RGB', (900, len(tipos)*356), FUNDO)
    d = ImageDraw.Draw(film)
    for row, tipo in enumerate(tipos):
        frames = sorted((PASTA / tipo).glob('frame_*.png'))
        dados = json.loads((PASTA / f'{tipo}_estados.json').read_text(encoding='utf-8'))
        assert len(frames) == len(dados['estados']) == 48, f'Sequência incompleta: {tipo}'
        video = PASTA / f'{tipo}.mp4'
        with av.open(str(video), 'w') as out:
            stream = out.add_stream('libx264', rate=15)
            stream.width, stream.height = 540, 960
            stream.pix_fmt = 'yuv420p'
            stream.options = {'crf': '14', 'preset': 'medium'}
            for f in frames:
                with Image.open(f) as img:
                    frame = av.VideoFrame.from_image(img.convert('RGB'))
                for packet in stream.encode(frame):
                    out.mux(packet)
            for packet in stream.encode():
                out.mux(packet)
        with av.open(str(video)) as check:
            n = sum(1 for _ in check.decode(video=0))
            assert n == len(frames)
        for col, idx in enumerate([0, 11, 23, 35, 47]):
            est = dados['estados'][idx]
            extra = f"λ={est['lam']:.2f}" if 'lam' in est else f"φ={est['fase_rotacao']:.2f} volta"
            d.text((180*col+5, 356*row+8), f'{tipo}  {extra}', font=FONT, fill='white')
            with Image.open(frames[idx]) as img:
                film.paste(img.convert('RGB').resize((180, 320)), (180*col, 356*row+36))
        resumo[tipo] = {'quadros': n, 'fps':15, 'duracao_s': n/15, 'bytes':video.stat().st_size,
                        'render_s':dados['segundos_render']}
    film.save(PASTA / 'sequencias.png')
    (PASTA / 'resumo.json').write_text(json.dumps(resumo,indent=2),encoding='utf-8')
    print(json.dumps(resumo,indent=2))


if __name__ == '__main__':
    main()
