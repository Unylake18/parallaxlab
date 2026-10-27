"""Troca somente N10/N11, copiando os pacotes H.264 dos demais blocos."""
import json
from fractions import Fraction
from pathlib import Path
import av

p = Path(__file__).resolve().parent
t = json.loads((p/'timing_repagina.json').read_text(encoding='utf-8'))
tp = json.loads((p/'timing_repagina_10_11.json').read_text(encoding='utf-8'))
blocos = {b['bloco']: b for b in t['blocos']}
inicio = round(blocos['N10']['inicio'] * 15)
fim = round(blocos['N11']['fim'] * 15)
assert round(tp['duracao'] * 15) == fim-inicio
origem = p/'media_repagina/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
ajuste = p/'media_repagina/ajuste/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
destino = p/'media_repagina/preview_repagina_0007_960x540_15fps.mp4'
temporario = destino.with_name('preview_repagina_temporario.mp4')
contagens = []
with av.open(str(origem)) as c, av.open(str(temporario),'w') as out:
    stream = out.add_stream_from_template(c.streams.video[0])
    stream.time_base = Fraction(1,15360)
    ultimo_dts = None
    for arquivo, lo, hi, deslocamento in [(origem,0,inicio,0),(ajuste,0,fim-inicio,inicio),(origem,fim,10**9,0)]:
        count=0
        with av.open(str(arquivo)) as entrada:
            for packet in entrada.demux(video=0):
                if packet.dts is None: continue
                pts = round(packet.pts*packet.time_base*15)
                dts = round(packet.dts*packet.time_base*15)
                if not lo <= pts < hi: continue
                packet.pts = (pts+deslocamento)*1024
                packet.dts = (dts+deslocamento)*1024
                assert ultimo_dts is None or packet.dts > ultimo_dts
                ultimo_dts = packet.dts
                packet.duration=1024; packet.time_base=stream.time_base; packet.stream=stream
                out.mux(packet); count+=1
        contagens.append(count)
assert sum(contagens) == round(t['duracao']*15), contagens
with av.open(str(temporario)) as c:
    assert c.streams.video[0].average_rate == 15
temporario.replace(destino)
print(f'Pacotes antes / N10-N11 / depois: {contagens}; sem recodificação.')
