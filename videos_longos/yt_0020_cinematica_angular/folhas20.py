"""yt_0020 v6 · folhas de contato: para ≥ 40 gatilhos (todos de T3-4, T5-6, E1-5, E1-6, E2-3 e H2), 5 quadros em t_voz −0,20, −0,12, 0, +0,20, +0,50.
Lê renders/sync.txt + ancoras.json. uso: python folhas20.py PREVIEW.mp4"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
ALV = {"T3-4", "T5-6", "E1-5", "E1-6", "E2-3", "H2"}
alv = []
for ln in (U / "renders" / "sync.txt").read_text(encoding="utf-8").split("## todos os gatilhos")[1].splitlines():
    m = re.match(r"(\S+)\s+([\d.]+)\s+([\d.]+)\s+([+-][\d.]+)\s+(.*)", ln)
    if m and m.group(1) in ALV:
        alv.append((m.group(1), float(m.group(2)), float(m.group(4)), m.group(5)))
OFS = [-0.20, -0.12, 0.0, 0.20, 0.50]
c = av.open(sys.argv[1])
s = c.streams.video[0]


def quadro(t):
    c.seek(int(max(t, 0) / s.time_base), stream=s)
    for fr in c.decode(s):
        if fr.time >= t - 0.034:
            return fr.to_image().resize((384, 216))


out = U / "renders" / "v6"
out.mkdir(parents=True, exist_ok=True)
POR = 8
for f0 in range(0, len(alv), POR):
    grupo = alv[f0:f0 + POR]
    img = Image.new("RGB", (5 * 384, len(grupo) * 246), (8, 12, 28))
    d = ImageDraw.Draw(img)
    for r, (aid, tv, dl, fr) in enumerate(grupo):
        t0 = anc[aid]["ini"] + tv
        d.text((4, r * 246 + 2), f"{aid} «{fr[:60]}»  t_voz={t0:.2f}s  delta={dl:+.2f}", fill=(255, 220, 120))
        for k, o in enumerate(OFS):
            im = quadro(t0 + o)
            img.paste(im, (k * 384, r * 246 + 24))
            d.text((k * 384 + 4, r * 246 + 26), f"{o:+.2f}", fill=(255, 255, 255))
    img.save(out / f"folha_{f0 // POR + 1:02d}.png")
print(len(alv), "gatilhos;", (len(alv) + POR - 1) // POR, "folhas")
