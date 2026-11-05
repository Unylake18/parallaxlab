"""G28 v3 (handoff v3 §3): prancha humana — os 24 quadros do preview com mais glifos no ESQUEMA + CONTA (linhas [dens] da auditoria, a cada 3
quadros), com pelo menos 4 s entre dois escolhidos do mesmo lote. Também grava renders/excluir_fundo.json (A1 e EN1 no preview) e
renders/v3/inicio_lotes.json (início de cada lote no preview).
uso: python prancha_humana.py [rodada]  → renders/<rodada>/prancha_humana_24.png"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
LOTES = ["PH", "PT1", "PT2", "PT3", "PT4", "PT5", "PE1", "PE2", "PE3", "PS"]
log = lambda l: (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
ini, t = {}, 0
for l in LOTES:
    ini[l] = t
    t += int(re.search(r"\[tempo\] total [0-9.]+ s \((\d+) quadros\)", log(l)).group(1))
(U / "renders" / RODADA).mkdir(parents=True, exist_ok=True)
(U / "renders" / RODADA / "inicio_lotes.json").write_text(json.dumps({k: v / 15 for k, v in ini.items()}), encoding="utf-8")
excl = []
for l, aid in (("PH", "A1"), ("PS", "EN1")):
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log(l))]
    for (a, t0), (_, t1) in zip(anc, anc[1:]):
        if a == aid:
            excl.append([round(ini[l] / 15 + t0 - 0.4, 2), round(ini[l] / 15 + t1 + 0.4, 2)])
(U / "renders" / "excluir_fundo.json").write_text(json.dumps(excl), encoding="utf-8")
cand = []
for l in LOTES:
    fa = U / f"log_aud_{l}.txt"
    for m in re.finditer(r"\[dens\] ([0-9.]+) (\d+)", fa.read_text(encoding="utf-8", errors="replace") if fa.exists() else log(l)):
        cand.append((int(m.group(2)), l, float(m.group(1))))
cand.sort(reverse=True)
esc = []
for n, l, tl in cand:
    if all(not (l == l2 and abs(tl - t2) < 4.0) for _, l2, t2 in esc):
        esc.append((n, l, tl))
    if len(esc) == 24:
        break
esc.sort(key=lambda e: ini[e[1]] + e[2] * 15)
alvo = {int(round(ini[l] + tl * 15)): (n, l, tl) for n, l, tl in esc}
c = av.open(str(U / "renders" / f"preview_yt0020_{RODADA}_960x540.mp4"))
ims = {}
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        ims[i] = fr.to_image()
    if i > max(alvo):
        break
W, H, C = 640, 360, 3
pr = Image.new("RGB", (W * C, (H + 20) * 8), "black")
d = ImageDraw.Draw(pr)
for k, q in enumerate(sorted(alvo)):
    n, l, tl = alvo[q]
    x, y = (k % C) * W, (k // C) * (H + 20)
    pr.paste(ims[q].resize((W, H)), (x, y + 20))
    d.text((x + 4, y + 4), f"{q / 15 // 60:.0f}:{q / 15 % 60:04.1f}  {l} {tl:.1f} s  · {n} glifos", fill="yellow")
pr.save(U / "renders" / RODADA / "prancha_humana_24.png")
print(json.dumps([(f"{q / 15 // 60:.0f}:{q / 15 % 60:04.1f}", alvo[q][1], alvo[q][0]) for q in sorted(alvo)], ensure_ascii=False))
