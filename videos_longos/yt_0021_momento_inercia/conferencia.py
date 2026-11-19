"""yt_0021: quadros de conferência do preview (handoff §6.4) e pranchas por bloco. Cada âncora: o quadro a 92% dela (conta montada).
uso: python conferencia.py [rodada] → renders/<rodada>/conferencia/<âncora>.png, renders/<rodada>/pranchas/P*.png"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v2"
q = json.loads((U / "renders" / f"quadros_{R}.json").read_text(encoding="utf-8"))
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem = anc["ordem"]
CONF = ["H2", "H3", "A3", "T1-3", "T1-4", "T2-1", "T2-4", "T3-3", "T4-3", "T4-4", "T5-2", "T5-3", "T5-4", "T6-3", "T6-4", "E1-2", "E1-4", "E2-3", "E2-4", "E3-3", "E3-5", "E3-6", "S2", "EN2"]
BLOCOS = {"PH": ["H1", "H2", "H3"], "PA": ["A1", "A2", "A3"], "PS-EN": ["S1", "S2", "EN1", "EN2"]}
for pre in ("T1", "T2", "T3", "T4", "T5", "T6", "E1", "E2", "E3"):
    BLOCOS["P" + pre] = [a for a in ordem if a.startswith(pre + "-")]
alvo = {}
for a in ordem:
    alvo.setdefault(q[a] + int(0.92 * anc["ancoras"][a]["dur"] * 15), []).append(a)
dc = U / "renders" / R / "conferencia"
dp = U / "renders" / R / "pranchas"
dc.mkdir(parents=True, exist_ok=True)
dp.mkdir(parents=True, exist_ok=True)
ims = {}
c = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        for a in alvo[i]:
            ims[a] = (i, fr.to_image())
for a in CONF:
    ims[a][1].save(dc / f"{a}.png")
for nome, ids in BLOCOS.items():
    W, H, C = 640, 360, 3
    Ln = (len(ids) + C - 1) // C
    pr = Image.new("RGB", (W * C, (H + 18) * Ln), "black")
    d = ImageDraw.Draw(pr)
    for k, a in enumerate(ids):
        x, y = (k % C) * W, (k // C) * (H + 18)
        i, im = ims[a]
        pr.paste(im.resize((W, H)), (x, y + 18))
        d.text((x + 4, y + 3), f"{a}  q{i}  {i // 15 // 60}:{i / 15 % 60:04.1f}", fill="yellow")
    pr.save(dp / f"{nome}.png")
print(len(CONF), "quadros de conferência;", len(BLOCOS), "pranchas")
