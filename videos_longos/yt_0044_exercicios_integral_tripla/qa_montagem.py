"""yt_0044 · QA da montagem (§8.3): quadros pretos, quadros por lote, e prancha das emendas (último quadro de um lote | primeiro do seguinte)."""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
V = U / "renders/v1/yt_0044_preview_v1_540p15.mp4"
ini = json.loads((U / "renders/v1/lotes_v1.json").read_text())["inicio"]
alvo = {q - 1 for q in ini.values() if q} | {q for q in ini.values()}
c = av.open(str(V))
n, pretos, ims = 0, [], {}
for fr in c.decode(video=0):
    a = fr.to_ndarray(format="rgb24")
    if a.mean() < 8:
        pretos.append(n)
    if n in alvo:
        ims[n] = Image.fromarray(a)
    n += 1
c.close()
pares = [(q - 1, q) for q in sorted(ini.values()) if q]
pr = Image.new("RGB", (960 * 2, 540 * len(pares)))
for i, (a, b) in enumerate(pares):
    pr.paste(ims[a], (0, 540 * i)); pr.paste(ims[b], (960, 540 * i))
(U / "renders/v1/qa").mkdir(parents=True, exist_ok=True)
pr.save(U / "renders/v1/qa/emendas_v1.jpg", quality=85)
out = [f"MONTAGEM: {n} quadros = {n / 15:.2f} s; ordem {list(ini)}", f"quadros pretos (média < 8): {len(pretos)} {pretos[:10]}",
       "emendas: renders/v1/qa/emendas_v1.jpg (último quadro do lote | primeiro do seguinte)"]
(U / "renders/v1/qa/montagem_v1.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
