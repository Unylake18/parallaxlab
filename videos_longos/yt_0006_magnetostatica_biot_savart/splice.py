"""Emenda de preview: uv run python splice.py SAIDA.mp4 vid:t0:t1 vid:t0:t1 ...  (t em segundos de cada vídeo; recodifica H.264 CRF 16)."""
import sys
import av
from fractions import Fraction

out, specs = sys.argv[1], sys.argv[2:]
o = av.open(out, "w", options={"movflags": "+faststart"})
st = o.add_stream("libx264", rate=15)
st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
st.options = {"crf": "16", "preset": "medium"}
n = 0
for sp in specs:
    p, a, b = sp.rsplit(":", 2)
    f0, f1 = round(float(a) * 15), (round(float(b) * 15) if float(b) >= 0 else 10**9)
    c = av.open(p)
    for i, fr in enumerate(c.decode(c.streams.video[0])):
        if i < f0:
            continue
        if i >= f1:
            break
        fr = fr.reformat(format="yuv420p")
        fr.pts = n
        fr.time_base = Fraction(1, 15)
        for pk in st.encode(fr):
            o.mux(pk)
        n += 1
    c.close()
for pk in st.encode():
    o.mux(pk)
o.close()
print("ok", n, n / 15)
