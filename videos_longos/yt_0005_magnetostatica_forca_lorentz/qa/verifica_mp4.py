"""Integridade do MP4: decodifica TODOS os quadros, confere resolução/fps/duração, tempos crescentes e lacunas."""
import sys, av
v = sys.argv[1]
c = av.open(v)
s = c.streams.video[0]
n, prev, gaps, nao_cresc, mx = 0, None, 0, 0, 0.0
for f in c.decode(s):
    t = float(f.pts * s.time_base)
    if prev is not None:
        d = t - prev
        if d <= 0:
            nao_cresc += 1
        if d > 0.05:
            gaps += 1
        mx = max(mx, d)
    prev = t
    n += 1
print("arquivo:", v)
print("resolução: %dx%d · fps: %.3f · quadros decodificados: %d · duração: %.2f s (%d:%05.2f)" % (s.width, s.height, float(s.average_rate), n, prev, int(prev) // 60, prev % 60))
print("tempos não crescentes: %d · lacunas > 50 ms: %d · maior intervalo: %.1f ms" % (nao_cresc, gaps, mx * 1000))
