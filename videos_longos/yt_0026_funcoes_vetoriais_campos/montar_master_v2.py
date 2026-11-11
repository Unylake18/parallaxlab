"""yt_0026 papel v2 (2026-11-11): master = vídeo novo (renders/yt_0026_sem_audio_1080p30.mp4, remux dos lotes) + o stream de ÁUDIO do master v9 entregue,
copiado pacote a pacote (sem decodificar nem recomprimir: mesma voz, mesmo sync). uso: python montar_master_v2.py MASTER_V9.mp4"""
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
vid = av.open(str(U / "renders" / "yt_0026_sem_audio_1080p30.mp4"))
aud = av.open(sys.argv[1])
out = av.open(str(U / "renders" / "yt_0026_master_final_1080p30.mp4"), "w")
sv, sa = vid.streams.video[0], aud.streams.audio[0]
ov, oa = out.add_stream_from_template(sv), out.add_stream_from_template(sa)
pk = [(p, ov) for p in vid.demux(sv) if p.dts is not None] + [(p, oa) for p in aud.demux(sa) if p.dts is not None]
pk.sort(key=lambda x: float(x[0].dts * x[0].time_base))
for p, s in pk:
    p.stream = s
    out.mux(p)
out.close()
print("video", float(sv.duration * sv.time_base) if sv.duration else sv.frames / 30, "s; audio", float(sa.duration * sa.time_base), "s")
