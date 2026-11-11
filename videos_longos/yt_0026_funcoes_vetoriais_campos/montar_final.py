"""yt_0026 v9: emenda os lotes 1080p30 (media1080_<C>) na ordem do vídeo, com B7, SEM reencodar (remux H.264) → renders/yt_0026_sem_audio_1080p30.mp4.
Depois: python ../../videos/montar_master.py renders/yt_0026_sem_audio_1080p30.mp4 audio/narracao_final.wav renders/yt_0026_master_final_1080p30.mp4"""
from pathlib import Path

import av

U = Path(__file__).resolve().parent
LOTES = ["PT", "PAH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
out = av.open(str(U / "renders" / "yt_0026_sem_audio_1080p30.mp4"), "w")
so, off, nq = None, 0, 0
for c_ in LOTES:
    c = av.open(str(U / f"media1080_{c_}/videos/cena/1080p30/{c_}.mp4"))
    s = c.streams.video[0]
    if so is None:
        so = out.add_stream_from_template(s)
    d = int(round(1 / (30 * s.time_base)))
    for p in c.demux(s):
        if p.dts is None:
            continue
        p.pts += off
        p.dts += off
        p.stream = so
        out.mux(p)
    off += s.frames * d
    nq += s.frames
    c.close()
out.close()
print(nq, "quadros;", round(nq / 30, 2), "s")
