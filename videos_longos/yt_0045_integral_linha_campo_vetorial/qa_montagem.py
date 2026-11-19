"""yt_0045 · QA da montagem (§8.3): quadros pretos, quadros por lote, e prancha das emendas (último quadro de um lote | primeiro do seguinte)."""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
V = U / "renders/final/yt_0045_preview_final_540p15.mp4"
ini = json.loads((U / "renders/final/lotes_final.json").read_text())["inicio"]
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
(U / "renders/final/qa").mkdir(parents=True, exist_ok=True)
pr.save(U / "renders/final/qa/emendas_final.jpg", quality=85)
out = [f"MONTAGEM: {n} quadros = {n / 15:.2f} s; ordem {list(ini)}", f"quadros pretos (média < 8): {len(pretos)} {pretos[:10]}",
       "emendas: renders/final/qa/emendas_final.jpg (último quadro do lote | primeiro do seguinte)"]
(U / "renders/final/qa/montagem_final.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))

# diferença média de fundo entre o último quadro de um lote e o primeiro do seguinte (faixas laterais x < 30 e x > 930, só papel): meta <= 1,0
import numpy as _np
dif = []
for a, b in pares:
    A_, B_ = _np.asarray(ims[a].convert("L"), float), _np.asarray(ims[b].convert("L"), float)
    m = _np.r_[A_[:, :30].ravel(), A_[:, 930:].ravel()], _np.r_[B_[:, :30].ravel(), B_[:, 930:].ravel()]
    dif.append(float(_np.abs(m[0] - m[1]).mean()))
msg = f"emendas: diferença média de fundo por emenda {[round(d, 2) for d in dif]}; maior {max(dif):.2f} (meta <= 1,0)"
print(msg)
open(U / "renders/final/qa/montagem_final.txt", "a", encoding="utf-8").write(chr(10) + msg + chr(10))
