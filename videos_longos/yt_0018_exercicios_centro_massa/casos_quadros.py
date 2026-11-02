"""v3 §10.3: os 14 quadros da §2 antes (preview v2) e depois (preview v3), no mesmo ponto da fala: o tempo do v2 vira (âncora, fração da
âncora) pelos logs da auditoria do v2 (log_aud_<LOTE>__teste_v2.txt) e volta para o v3 pela mesma âncora (log_<LOTE>.txt do v3).
uso: python casos_quadros.py → renders/v3/casos_antes_depois.png e renders/v3/casos/caso_N_{antes,depois}.png"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
from casos14 import CASOS, INICIO_V2  # noqa: E402

ini3 = json.loads((U / "renders" / "v3" / "inicio_lotes.json").read_text(encoding="utf-8"))
anc = lambda f: [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", f.read_text(encoding="utf-8", errors="replace"))]
alvo2, alvo3 = {}, {}
for n, tv2, lote, _, desc in CASOS:
    tl = tv2 - INICIO_V2[lote]
    a2 = anc(U / f"log_aud_{lote}__teste_v2.txt")
    a3 = dict(zip([a for a, _ in anc(U / f"log_{lote}.txt")], zip([t for _, t in anc(U / f"log_{lote}.txt")], [t for _, t in anc(U / f"log_{lote}.txt")][1:] + [9e9])))
    k = max(i for i, (a, t) in enumerate(a2) if t <= tl + 1e-6) if tl >= 0 else 0
    aid, t0 = a2[k]
    t1 = a2[k + 1][1] if k + 1 < len(a2) else t0 + 5
    fr = (tl - t0) / max(t1 - t0, 1e-6)
    s3, e3 = a3.get(aid, (0.0, 1.0))
    t3 = ini3[lote] + s3 + fr * (min(e3, s3 + 60) - s3)
    alvo2[n] = int(round(max(tv2, 0) * 15))
    alvo3[n] = (int(round(t3 * 15)), aid, fr, desc)


def quadros(arq, qs):
    c = av.open(str(arq))
    out, mx = {}, max(qs)
    for i, f in enumerate(c.decode(video=0)):
        if i in qs:
            out[i] = f.to_image()
        if i > mx:
            break
    return out


q2 = quadros(U / "renders" / "preview_yt0018_v2_960x540.mp4", set(alvo2.values()))
q3 = quadros(U / "renders" / "preview_yt0018_v3_960x540.mp4", {v[0] for v in alvo3.values()})
(U / "renders" / "v3" / "casos").mkdir(parents=True, exist_ok=True)
W, H = 640, 360
pr = Image.new("RGB", (2 * W + 10, 14 * (H + 22)), "black")
d = ImageDraw.Draw(pr)
for k, (n, *_r) in enumerate(CASOS):
    a, b = q2[alvo2[n]], q3[alvo3[n][0]]
    a.save(U / "renders" / "v3" / "casos" / f"caso_{n:02d}_antes.png")
    b.save(U / "renders" / "v3" / "casos" / f"caso_{n:02d}_depois.png")
    y = k * (H + 22)
    pr.paste(a.resize((W, H)), (0, y + 22))
    pr.paste(b.resize((W, H)), (W + 10, y + 22))
    q, aid, fr, desc = alvo3[n]
    d.text((4, y + 5), f"#{n} ANTES v2 {alvo2[n] / 15 // 60:.0f}:{alvo2[n] / 15 % 60:04.1f}  ({aid} {fr:.2f})  {desc}", fill="yellow")
    d.text((W + 14, y + 5), f"DEPOIS v3 {q / 15 // 60:.0f}:{q / 15 % 60:04.1f}", fill="yellow")
pr.save(U / "renders" / "v3" / "casos_antes_depois.png")
print("ok")
