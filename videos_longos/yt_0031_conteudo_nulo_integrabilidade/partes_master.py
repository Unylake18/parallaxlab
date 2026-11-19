"""yt_0031: divide o master 1080p30 em partes tocáveis (< 28 MiB cada), sem reencodar (remux, corte no keyframe), para enviar pelo chat.
Saída: renders/partes_master/yt_0031_master_parte_N.mp4"""
from pathlib import Path

import av

U = Path(__file__).resolve().parent
SRC = U / "renders" / "yt_0031_master_final_1080p30.mp4"
OUT = U / "renders" / "partes_master"
OUT.mkdir(parents=True, exist_ok=True)
LIM = 27 * 2**20
src = av.open(str(SRC))
vi, ai = src.streams.video[0], src.streams.audio[0]
k, o, ov, oa, tam, t0v, t0a = 0, None, None, None, 0, 0, 0
saidas = []


def nova(pv, pa):
    global k, o, ov, oa, tam, t0v, t0a
    if o:
        o.close()
    k += 1
    p = OUT / f"yt_0031_master_parte_{k}.mp4"
    saidas.append(p)
    o = av.open(str(p), "w")
    ov = o.add_stream_from_template(vi)
    oa = o.add_stream_from_template(ai)
    tam, t0v, t0a = 0, pv, pa


pend_a = []
for pk in src.demux(vi, ai):
    if pk.dts is None:
        continue
    if pk.stream is vi:
        if o is None or (pk.is_keyframe and tam > LIM - 3 * 2**20):
            ta = int(float(pk.pts * vi.time_base) / ai.time_base)
            nova(pk.pts, ta)
        pk.pts -= t0v
        pk.dts -= t0v
        pk.stream = ov
    else:
        if o is None:
            continue
        pk.pts -= t0a
        pk.dts -= t0a
        if pk.pts < 0:
            continue
        pk.stream = oa
    o.mux(pk)
    tam += pk.size
o.close()
for p in saidas:
    with av.open(str(p)) as c:
        print(p.name, round(p.stat().st_size / 2**20, 1), "MiB", round(float(c.duration) / 1e6, 1), "s")
