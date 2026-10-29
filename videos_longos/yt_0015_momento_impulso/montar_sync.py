"""yt_0015 — preview sincronizado: os lotes nos quadros globais da voz + audio/narracao_v4.wav sem silêncio inserido.

Cada parte começa no seu quadro global (Manim: F0 do lote = S da 1ª âncora − header; 3D: S da 1ª âncora) e vai até o início da
seguinte; a diferença (±1 quadro de arredondamento) é cortada ou completada com o último quadro, e relatada.
Saída: renders/preview_yt0015_sync_960x540.mp4 (H.264 CRF 14 + AAC 192 kb/s), renders/preview_yt0015_sync_partes.json.
Uso: uv run --no-sync python montar_sync.py
"""
import json
import sys
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
FINAL = "--final" in sys.argv                    # render final: 1920×1080 / 30 fps, só vídeo (o master cola a voz depois)
FPS = 30 if FINAL else 15
RES = (1920, 1080) if FINAL else (960, 540)
SUF = f"{RES[0]}x{RES[1]}"
MAPA = json.loads((U / "sync" / "mapa.json").read_text(encoding="utf-8"))
PRE = json.loads((U / "sync" / "pre.json").read_text(encoding="utf-8"))
M = lambda c: U / f"media_{c}/videos/cena/{RES[1]}p{FPS}/{c}.mp4"
S = lambda a: round(MAPA["ancoras"][a]["S"] * FPS)
partes = [("hook", U / f"renders/hook_{SUF}.mp4", S("H1")), ("PA", M("PA"), S("A1") - PRE.get("A1", 0) * FPS // 15)]
for c, a in [("PT1", "T1-1"), ("PB", None), ("PT3", "T3-1"), ("PC", None), ("PD", "T5-1"), ("PE", "E1-1"), ("PF", None)]:
    partes.append((c, M(c), None))
partes += [("E4-1", U / f"renders/e4_{SUF}.mp4", S("E4-1")), ("PG", M("PG"), None), ("PS", M("PS"), None),
           ("F2", U / f"renders/cavalo_{SUF}.mp4", S("F2"))]
rec = {}
for i, (c, arq, g0) in enumerate(partes):
    if g0 is None:                                  # lote Manim: o 1º ponto gravado no passe SYNC diz a âncora de entrada
        r = json.loads((U / "sync" / f"rec_{c}.json").read_text(encoding="utf-8"))
        a0 = r["pontos"][0]["aid"]
        partes[i] = (c, arq, S(a0) - PRE.get(a0, 0) * FPS // 15)
N = round(MAPA["fim"] * FPS)
saida = U / "renders" / ("video_final_yt0015_1920x1080_30fps.mp4" if FINAL else "preview_yt0015_sync_960x540.mp4")
out = av.open(str(saida), "w")
vs = out.add_stream("libx264", rate=Fraction(FPS))
vs.width, vs.height, vs.pix_fmt = RES[0], RES[1], "yuv420p"
vs.options = {"crf": "14", "preset": "medium"}
if not FINAL:
    aus = out.add_stream("aac", rate=44100)
    aus.layout = "mono"
    aus.bit_rate = 192000
marcas, t = [], 0
for k, (nome, arq, g0) in enumerate(partes):
    g1 = partes[k + 1][2] if k + 1 < len(partes) else N
    assert g0 == t, (nome, g0, t)
    c = av.open(str(arq))
    n, last = 0, None
    for fr in c.decode(video=0):
        if n >= g1 - g0:
            n += 1
            continue
        img = fr.to_ndarray(format="rgb24")
        for p in vs.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        last, n = img, n + 1
    c.close()
    usados = min(n, g1 - g0)
    for _ in range(g1 - g0 - usados):
        for p in vs.encode(av.VideoFrame.from_ndarray(last, format="rgb24")):
            out.mux(p)
    marcas.append({"parte": nome, "ini_s": round(g0 / FPS, 2), "dur_s": round((g1 - g0) / FPS, 2), "quadros_lote": n,
                   "dif_quadros": n - (g1 - g0)})
    t = g1
for p in vs.encode():
    out.mux(p)
if FINAL:
    out.close()
    (U / "renders" / "video_final_partes.json").write_text(json.dumps(marcas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"saida": str(saida), "quadros": N, "duracao_s": round(N / FPS, 3)}, ensure_ascii=False))
    for m in marcas:
        print(f"  {m['parte']:5s} {m['ini_s']:8.2f} s  {m['dur_s']:7.2f} s  lote {m['quadros_lote']:6d} q  dif {m['dif_quadros']:+d}")
    sys.exit(0)
with wave.open(str(U / "audio" / "narracao_v4.wav"), "rb") as w:
    assert w.getframerate() == 44100 and w.getnchannels() == 1
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
alvo = round(N / FPS * 44100)
a = np.concatenate([a, np.zeros(max(0, alvo - len(a)), np.int16)])[:alvo]
pts = 0
for i in range(0, len(a), 1024):
    fr = av.AudioFrame.from_ndarray(a[i:i + 1024].reshape(1, -1), format="s16", layout="mono")
    fr.sample_rate, fr.pts = 44100, pts
    pts += fr.samples
    for p in aus.encode(fr):
        out.mux(p)
for p in aus.encode():
    out.mux(p)
out.close()
(U / "renders" / "preview_yt0015_sync_partes.json").write_text(json.dumps(marcas, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": N, "duracao_s": round(N / FPS, 2)}, ensure_ascii=False))
for m in marcas:
    print(f"  {m['parte']:5s} {m['ini_s']:8.2f} s  {m['dur_s']:7.2f} s  lote {m['quadros_lote']:6d} q  dif {m['dif_quadros']:+d}")
