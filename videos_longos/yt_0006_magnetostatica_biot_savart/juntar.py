"""Junta os trechos do preview recodificando (H.264, yuv420p, CRF 16): uv run python juntar.py SAIDA.mp4 T1.mp4 T2.mp4 ..."""
import sys
import av
from fractions import Fraction

out, parts = sys.argv[1], sys.argv[2:]
o = av.open(out, "w", options={"movflags": "+faststart"})
st = o.add_stream("libx264", rate=15)
st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
st.options = {"crf": "16", "preset": "medium"}
n = 0
for p in parts:
    c = av.open(p)
    for fr in c.decode(c.streams.video[0]):
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
