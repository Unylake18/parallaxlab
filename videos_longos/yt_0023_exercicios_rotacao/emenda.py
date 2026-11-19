"""emenda.py LOTE q0 q1 trecho.mp4 — troca os quadros [q0,q1) do preview do lote pelos do trecho (re-codifica em CRF 23, 540p/15 fps)."""
import av, sys, os, shutil
L, q0, q1, tr = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
mp = f"media_{L}/videos/cena/540p15/{L}.mp4"
bk = mp.replace(".mp4", ".antes_trecho.mp4")
if not os.path.exists(bk): shutil.copy(mp, bk)
src = av.open(bk); t = av.open(tr)
n_t = sum(1 for _ in t.decode(video=0)); t.close(); t = av.open(tr)
assert n_t == q1 - q0, f"trecho tem {n_t} quadros, esperado {q1 - q0}"
out = av.open(mp + ".tmp.mp4", "w")
s = out.add_stream("libx264", rate=15); s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"; s.options = {"crf": "23"}
tf = t.decode(video=0)
for i, f in enumerate(src.decode(video=0)):
    g = next(tf) if q0 <= i < q1 else f
    nf = av.VideoFrame.from_ndarray(g.to_ndarray(format="rgb24"), format="rgb24"); nf.pts = i
    for p in s.encode(nf): out.mux(p)
for p in s.encode(): out.mux(p)
out.close(); src.close(); t.close()
os.replace(mp + ".tmp.mp4", mp)
print("emendado", mp, q0, q1)
