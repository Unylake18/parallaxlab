"""yt_0021 v9: folhas de contato dos gatilhos (handoff v8 §7.5.2). Para cada gatilho escolhido, 5 quadros do preview v9 em
t_voz − 0,20 · − 0,12 · t_voz · + 0,20 · + 0,50 s (preview a 15 fps: quadro mais próximo). Lê renders/sync.txt (seção "todos").
Grava renders/v9/sync/folha_NN.jpg e renders/v9/sync/indice.txt. uso: python folhas_sync21.py [v9]"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v9"
FPS = 15
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
txt = (U / "renders" / "sync.txt").read_text(encoding="utf-8")
todos = txt.split("todos:")[1].strip().splitlines()
lin = []
for l in todos:
    m = re.match(r"\s+(\S+)\s+(.*?)\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+([+-][0-9.]+)\s*$", l)
    if m:
        lin.append((m.group(1), m.group(2).strip(), float(m.group(3)), float(m.group(4)), float(m.group(5))))
# todos os gatilhos das âncoras críticas do §7.4 + os de valores do H2 e demais com número falado
CRIT = {"T4-3", "T5-5", "T5-6", "E1-4", "E2-5", "S2", "H2", "T4-4", "T5-3", "E2-1", "E2-3", "E2-6"}
esc = [x for x in lin if x[0] in CRIT]
DT = [-0.20, -0.12, 0.0, 0.20, 0.50]
need = {}
for aid, fr, tv, ti, d in esc:
    base = ANC[aid]["ini"] + tv
    for k in DT:
        need[round((base + k) * FPS)] = None
c = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
for i, fr in enumerate(c.decode(video=0)):
    if i in need:
        need[i] = fr.to_image().resize((384, 216))
    if i > max(need):
        break
out = U / "renders" / R / "sync"
out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*"):
    f.unlink()
fonte = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
POR = 8
idx = []
for s0 in range(0, len(esc), POR):
    grupo = esc[s0:s0 + POR]
    folha = Image.new("RGB", (384 * 5, 236 * len(grupo)), (10, 14, 28))
    dr = ImageDraw.Draw(folha)
    for r_, (aid, fr, tv, ti, d) in enumerate(grupo):
        base = ANC[aid]["ini"] + tv
        for c_, k in enumerate(DT):
            im = need.get(round((base + k) * FPS))
            if im is not None:
                folha.paste(im, (384 * c_, 236 * r_ + 20))
            dr.text((384 * c_ + 4, 236 * r_ + 2), f"{k:+.2f} s" + ("  ← PALAVRA" if k == 0 else ""), font=fonte, fill=(255, 220, 120))
        dr.text((384 * 2 + 150, 236 * r_ + 2), f"{aid} · {fr[:48]} · t_voz {tv:.2f} · imagem {ti:.2f} · Δ {d:+.2f}", font=fonte, fill=(160, 240, 255))
    n = s0 // POR + 1
    folha.save(out / f"folha_{n:02d}.jpg", quality=88)
    idx += [f"folha_{n:02d}  {aid} · {fr} · t_voz {tv:.2f} · Δ {d:+.2f}" for aid, fr, tv, ti, d in grupo]
(out / "indice.txt").write_text("\n".join(idx), encoding="utf-8")
print(len(esc), "gatilhos;", (len(esc) + POR - 1) // POR, "folhas")
