import sys, av, numpy as np
sys.path.insert(0, ".")
import congelamento as C
def run(path, lim, thr):
    c = av.open(path); ant = None; fr_ = []
    for f in c.decode(video=0):
        g = f.to_ndarray(format="gray").astype(np.int16)
        if ant is not None: fr_.append(float((np.abs(g - ant) > lim).mean()))
        ant = g
    fr_ = np.array(fr_); parado = np.concatenate([[False], fr_ < thr])
    runs = C.corridas(parado, C.D_); fala = C.na_fala(runs)
    return fala
for lim, thr in ((10, 1e-4), (10, 3e-4)):
    for nome, p in (("preview", "renders/preview_yt0018_v7mudo_960x540.mp4"), ("final-decim", "renders/final/_decim_960x540_15.mp4")):
        f = run(p, lim, thr)
        print(f"lim {lim}/255, frac<{thr}: {nome:12s} {len(f):3d} trechos, {sum(d for _, d in f):6.1f} s, maior {max([d for _, d in f], default=0):.1f} s")
print([x for x in run("renders/final/_decim_960x540_15.mp4", 10, 1e-4)])
