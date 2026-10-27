"""Reconforma o preview completo com blocos revistos, preservando os outros renders.

Não produz master: só um preview silencioso 960×540/15 fps, em CRF 14.
As entradas e saídas ficam exclusivamente nesta unidade.
"""

from fractions import Fraction
import json
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
FPS = 15


def quadros(caminho, inicio, fim):
    primeiro, ultimo = round(inicio * FPS), round(fim * FPS)
    with av.open(str(caminho)) as container:
        stream = container.streams.video[0]
        container.seek(int(inicio / float(stream.time_base)), stream=stream, backward=True)
        for frame in container.decode(stream):
            numero = round(float(frame.time) * FPS)
            if numero < primeiro:
                continue
            if numero >= ultimo:
                break
            yield frame


def montar():
    base = PASTA / 'media_preview/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
    original = json.loads((PASTA / 'timing_preview.json').read_text(encoding='utf-8'))
    patches = {}
    for pasta, nome in (('media_revisao', 'timing_parcial_1_3_9_13_15_18.json'),
                         ('media_ajuste09', 'timing_parcial_9.json'),
                         ('media_ajuste17', 'timing_parcial_17.json')):
        parcial = json.loads((PASTA / nome).read_text(encoding='utf-8'))
        for j, b in enumerate(parcial['blocos']):
            patches[b['bloco']] = dict(b, primeiro=j == 0, marcos=parcial['marcos'],
                arquivo=PASTA / pasta / 'videos/cena/540p15/OrbitaQuedaContinua007.mp4')
    destino = PASTA / 'media_preview/preview_completo_0007_960x540_15fps.mp4'
    saida_timing = dict(blocos=[], marcos=[], fps=FPS, segmentos=[])
    contador = 0
    with av.open(str(destino), mode='w') as output:
        stream = output.add_stream('libx264', rate=FPS, options={'crf': '14', 'preset': 'medium'})
        stream.width, stream.height, stream.pix_fmt = 960, 540, 'yuv420p'
        for i, bloco in enumerate(original['blocos']):
            inicio_novo = contador / FPS
            patch = patches.get(bloco['bloco'])
            anterior_revisado = i > 0 and original['blocos'][i-1]['bloco'] in patches
            if patch:
                # A saída do bloco anterior deve vir do filme completo, não
                # do bloco anterior (diferente) do render parcial.
                fade_original = .6 if i and not anterior_revisado else 0
                fade_parcial = 0 if patch['primeiro'] else .6
                segmentos = []
                if fade_original:
                    segmentos.append((base, bloco['inicio'], bloco['inicio'] + fade_original))
                segmentos.append((patch['arquivo'], patch['inicio'] + fade_parcial, patch['fim']))
                marcos = [m for m in patch['marcos'] if patch['inicio'] <= m['tempo'] <= patch['fim']]
                deslocamento = inicio_novo + fade_original - patch['inicio'] - fade_parcial
            else:
                # Corte editorial após um bloco revisto: não ressuscitar, no
                # fade antigo, um quadro da versão anterior daquele bloco.
                corte = .6 if anterior_revisado else 0
                segmentos = [(base, bloco['inicio'] + corte, bloco['fim'])]
                marcos = [m for m in original['marcos'] if bloco['inicio'] <= m['tempo'] <= bloco['fim']]
                deslocamento = inicio_novo - bloco['inicio'] - corte
            for caminho, inicio, fim in segmentos:
                esperados = round(fim * FPS) - round(inicio * FPS)
                escritos = 0
                for frame in quadros(caminho, inicio, fim):
                    frame.pts = contador
                    frame.time_base = Fraction(1, FPS)
                    frame.pict_type = av.video.frame.PictureType.NONE
                    for packet in stream.encode(frame):
                        output.mux(packet)
                    contador += 1
                    escritos += 1
                assert escritos == esperados, (bloco['bloco'], escritos, esperados)
                saida_timing['segmentos'].append(dict(bloco=bloco['bloco'], fonte=str(caminho),
                                                       inicio=inicio, fim=fim, quadros=escritos))
            saida_timing['blocos'].append(dict(bloco=bloco['bloco'], inicio=inicio_novo, fim=contador / FPS))
            saida_timing['marcos'].extend(dict(nome=m['nome'], tempo=m['tempo'] + deslocamento) for m in marcos)
        for packet in stream.encode():
            output.mux(packet)
    saida_timing['duracao'] = contador / FPS
    (PASTA / 'timing_preview_revisado.json').write_text(json.dumps(saida_timing,
        indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(dict(preview=str(destino.resolve()), quadros=contador,
                          duracao=contador / FPS), ensure_ascii=False))


if __name__ == '__main__':
    montar()
