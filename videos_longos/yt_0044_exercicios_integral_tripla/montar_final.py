"""yt_0044 final (copiado do montar_final.py do yt_0032): emenda os lotes 1080p30 (media1080_<C>) na ordem do vídeo, SEM reencodar (remux H.264)
→ renders/yt_0044_sem_audio_1080p30.mp4. Depois:
uv run python ../../videos/montar_master.py renders/yt_0044_sem_audio_1080p30.mp4 audio/narracao_final.wav renders/yt_0044_master_final_1080p30.mp4"""
from pathlib import Path

import av

U = Path(__file__).resolve().parent
LOTES = ["PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"]
out = av.open(str(U / "renders" / "yt_0044_sem_audio_1080p30.mp4"), "w")
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
    print(f"[montar_final] {c_}: {s.frames} quadros")
    c.close()
out.close()
print(nq, "quadros;", round(nq / 30, 2), "s")
