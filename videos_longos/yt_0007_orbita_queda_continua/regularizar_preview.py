"""Regulariza timestamps de concatenação do Manim sem recodificar H.264."""
from fractions import Fraction
from pathlib import Path
import av

PASTA = Path(__file__).resolve().parent
origem = PASTA / 'media_repagina/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
destino = PASTA / 'media_repagina/preview_repagina_0007_960x540_15fps.mp4'

with av.open(str(origem)) as entrada, av.open(str(destino), 'w') as saida:
    s = entrada.streams.video[0]
    out = saida.add_stream_from_template(s)
    tb = Fraction(1, 15360)
    out.time_base = tb
    count = 0
    for packet in entrada.demux(s):
        if packet.dts is None: continue
        pt = round(packet.pts * packet.time_base * 15)
        dt = round(packet.dts * packet.time_base * 15)
        packet.pts = pt * 1024
        packet.dts = dt * 1024
        packet.duration = 1024
        packet.time_base = tb
        packet.stream = out
        saida.mux(packet)
        count += 1
with av.open(str(destino)) as c:
    s = c.streams.video[0]
    assert s.average_rate == 15, s.average_rate
    assert s.frames == count
print(f'{count} pacotes preservados; 15 fps exatos; sem recodificação: {destino}')
