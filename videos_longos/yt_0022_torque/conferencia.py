"""yt_0022: quadros de conferência do preview (handoff §8.4) e pranchas por bloco. Cada âncora: o quadro a 92% dela (conta montada).
uso: python conferencia.py [rodada] → renders/<rodada>/conferencia/<âncora>.png, renders/<rodada>/pranchas/P*.png"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
q = json.loads((U / "renders" / f"quadros_{R}.json").read_text(encoding="utf-8"))
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem = anc["ordem"]
CONF = ["H2", "A2", "T1-3", "T2-2", "T3-3", "T3-5", "T3-6", "T4-2", "T4-3", "T4-4", "T4-5", "T5-2", "T5-4", "T6-1", "T6-2", "S2"]
BLOCOS = {"PH": ["H1", "H2", "H3"], "PA": ["A1", "A2", "A3"], "PS": ["S1", "S2", "EN1", "EN2"]}
for pre in ("T1", "T2", "T3", "T4", "T5", "T6"):
    BLOCOS["P" + pre] = [a for a in ordem if a.startswith(pre + "-")]
alvo = {}
for a in ordem:
    alvo.setdefault(q[a] + int(0.92 * anc["ancoras"][a]["dur"] * 15), []).append(a)
dc = U / "renders" / R / "conferencia"
dp = U / "renders" / R / "pranchas"
dc.mkdir(parents=True, exist_ok=True)
dp.mkdir(parents=True, exist_ok=True)
ims = {}
c = av.open(str(U / "renders" / f"preview_yt0022_{R}_960x540.mp4"))
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
