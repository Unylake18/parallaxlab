"""Inspeção técnica e extração dos quadros de QA desta unidade, sem recodificar vídeo."""

import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

PASTA = Path(__file__).resolve().parent


def verificar(video=None, timing=None, saida='qa_preview'):
    video = Path(video) if video else PASTA / 'media_preview/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
    timing = Path(timing) if timing else PASTA / 'timing_preview.json'
    destino = PASTA / saida
    destino.mkdir(exist_ok=True)
    dados = json.loads(timing.read_text(encoding='utf-8'))
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        duracao = float(stream.duration * stream.time_base)
        info = dict(arquivo=str(video.resolve()), largura=stream.width, altura=stream.height,
                    fps=float(stream.average_rate), duracao=duracao, frames=stream.frames,
                    codec=stream.codec_context.name, pixel_format=stream.codec_context.format.name,
                    faixas_audio=len(container.streams.audio))
        cabecalho = b''.join(bytes(p) for _, p in zip(range(4), container.demux(stream)))
        crf = re.search(rb'crf=([0-9.]+)', cabecalho)
        info['crf'] = float(crf.group(1)) if crf else None
    assert (info['largura'], info['altura'], info['fps']) == (960, 540, 15)
    assert info['faixas_audio'] == 0
    assert abs(duracao - dados['duracao']) < .2
    alvos = [(b['bloco'] + '_final', max(b['inicio'], b['fim'] - 2)) for b in dados['blocos']]
    # O marco registra o estado concluído. Capturar antes dele confundia o
    # ajuste ainda elíptico com a condição aberta/circular que vem a seguir.
    alvos += [(m['nome'], min(duracao - 1/info['fps'], m['tempo'] + 1/info['fps']))
              for m in dados['marcos']]
    alvos.sort(key=lambda x: x[1])
    quadros = []
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        indice = 0
        for frame in container.decode(stream):
            instante = float(frame.time)
            while indice < len(alvos) and instante >= alvos[indice][1]:
                nome, alvo = alvos[indice]
                imagem = frame.to_image()
                imagem.save(destino / f'{nome}.png')
                quadros.append((nome, instante, imagem.copy()))
                indice += 1
    assert len(quadros) == len(alvos), (len(quadros), len(alvos))
    # Seis quadros por prancha; abrir os PNG individuais para conferir tipografia.
    for inicio in range(0, len(quadros), 6):
        grupo = quadros[inicio:inicio+6]
        prancha = Image.new('RGB', (1440, 580), '#111827')
        draw = ImageDraw.Draw(prancha)
        for i, (nome, instante, imagem) in enumerate(grupo):
            x, y = (i % 3) * 480, (i // 3) * 290
            prancha.paste(imagem.resize((480, 270)), (x, y + 20))
            draw.text((x+8, y+4), f'{nome} / {instante:.2f}s', fill='white')
        prancha.save(destino / f'prancha_{inicio//6+1:02d}.jpg', quality=95)
    info['quadros_extraidos'] = len(quadros)
    info['blocos'] = len(dados['blocos'])
    (destino / 'tecnico.json').write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--video')
    parser.add_argument('--timing')
    parser.add_argument('--saida', default='qa_preview')
    args = parser.parse_args()
    verificar(args.video, args.timing, args.saida)
