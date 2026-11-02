"""v4 §4: brilho da água por cena (hook e X3) e o percentil 99 da coluna de reflexo da lua no hook → renders/v4/agua.json.
Água: quadros do lago (registro `lago` do qa_overlay), 1 a cada 3, no vídeo do lote; metade de baixo do quadro: luminância média (meta ≥ 0,09)
e fração de pixels abaixo de 0,03 (meta ≤ 5%), por âncora. Lua: no hook (0–20 s), a faixa vertical de 60 px mais clara da metade de baixo;
percentil 99 do canal mais claro dentro dela (meta < 235, coluna azulada). uso: python agua.py [rodada]  (padrão: v5)"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
ROD = sys.argv[1] if len(sys.argv) > 1 else "v7"
out = {"agua": {}, "lua": {}}
for lote in ("PH", "PX3"):
    ov = json.loads((U / f"qa_overlay_{lote}.json").read_text(encoding="utf-8")).get("lago", {})
    lago = set(int(k) for k in ov)
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)]
    por = {}
    col = []
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    for i, fr in enumerate(c.decode(video=0)):
        t = i / 15
        if lote == "PH" and t <= 20.0 and i % 2 == 0:
            a = fr.to_ndarray(format="rgb24").astype(float)
            b = a[270:]
            Yc = (0.2126 * b[..., 0] + 0.7152 * b[..., 1] + 0.0722 * b[..., 2]).mean(axis=0)
            k = int(np.convolve(Yc, np.ones(60) / 60, mode="valid").argmax())
            faixa = b[:, k:k + 60]
            col.append((round(t, 2), float(np.percentile(faixa.max(axis=2), 99)), [int(x) for x in faixa.reshape(-1, 3).mean(axis=0)]))
        if i % 3 or i not in lago:
            continue
        a = fr.to_ndarray(format="rgb24").astype(float) / 255
        Y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        h = Y[270:]
        aid = next((x for x, t0 in reversed(anc) if t0 <= t + 1e-6), "?")
        if aid == "A1":
            continue                                                                  # A1 é o logo: os 3 quadros de transição do lago não contam
        por.setdefault(aid, []).append((float(h.mean()), float((h < 0.03).mean())))
    c.close()
    for aid, v in por.items():
        v = np.array(v)
        out["agua"][f"{lote} {aid}"] = {"quadros": len(v), "media_baixo": round(float(v[:, 0].mean()), 4), "min_media": round(float(v[:, 0].min()), 4),
                                        "frac_escuro": round(float(v[:, 1].mean()), 4), "max_frac": round(float(v[:, 1].max()), 4)}
    if col:
        pior = max(col, key=lambda q: q[1])
        out["lua"] = {"quadros": len(col), "p99_max": round(pior[1], 1), "t_pior": pior[0], "rgb_medio_faixa_pior": pior[2]}
(U / "renders" / ROD).mkdir(parents=True, exist_ok=True)
(U / "renders" / ROD / "agua.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(out, indent=1, ensure_ascii=False))
