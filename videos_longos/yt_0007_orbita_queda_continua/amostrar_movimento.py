"""Pranchas temporais do vídeo efetivamente codificado, para revisão de câmera."""
import argparse
import json
from pathlib import Path
import av
from PIL import Image, ImageDraw


def amostrar(video, timing, saida):
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    dados = json.loads(Path(timing).read_text(encoding='utf-8'))
    alvos = []
    for bloco in dados['blocos']:
        # A sequência inclui o corpo em trânsito, além dos estados finais.
        for i in range(12):
            t = bloco['inicio'] + (bloco['fim'] - bloco['inicio']) * (i + .5) / 12
            alvos.append((t, bloco['bloco'], i))
    extraidos = {}
    idx = 0
    with av.open(str(video)) as container:
        for frame in container.decode(video=0):
            t = float(frame.time)
            while idx < len(alvos) and t >= alvos[idx][0]:
                _, bloco, i = alvos[idx]
                im = frame.to_image()
                im.save(saida / f'{bloco}_mov_{i+1:02d}.png')
                extraidos.setdefault(bloco, []).append((t, im))
                idx += 1
    assert idx == len(alvos), (idx, len(alvos))
    for bloco, quadros in extraidos.items():
        prancha = Image.new('RGB', (1920, 870), '#111827')
        draw = ImageDraw.Draw(prancha)
        for i, (t, im) in enumerate(quadros):
            x, y = i % 4 * 480, i // 4 * 290
            prancha.paste(im.resize((480, 270)), (x, y+20))
            draw.text((x+8, y+4), f'{bloco} / {t:.2f}s', fill='white')
        prancha.save(saida / f'movimento_{bloco}.jpg', quality=95)
    print(f'{idx} amostras temporais, {len(extraidos)} pranchas: {saida}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--video', required=True)
    p.add_argument('--timing', required=True)
    p.add_argument('--saida', required=True)
    a = p.parse_args()
    amostrar(a.video, a.timing, a.saida)
