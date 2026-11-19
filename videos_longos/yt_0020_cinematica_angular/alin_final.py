"""yt_0020 · alinhamento Three.js × Manim a 1080p. O Manim (overlay do QA do preview, unidades de cena) é a verdade; o Three.js 1080p30 tem de cair no mesmo ponto: overlay gravado pelo próprio render 1080p30 (mesmo índice de quadro)."""
import json
from pathlib import Path
import numpy as np
U = Path(__file__).resolve().parent
tpx = lambda q: np.array([(q[0] + 8) / 16 * 1920, (4.5 - q[1]) / 9 * 1080])
out = []
for l in ("PH", "PT4", "PS"):
    f_ = U / "threejs/q3d" / f"{l}_1920x1080/helice/pontos.json"
    o_ = U / f"qa_overlay_{l}.json"
    if not f_.exists() or not o_.exists():
        out.append(f"{l}: sem dados"); continue
    pj = json.loads(f_.read_text(encoding="utf-8")); ov = json.loads(o_.read_text(encoding="utf-8"))
    regs = []
    for f, v in ov.get("helice", {}).items(): regs.append((int(f), v))
    for f, v in ov.get("helice6", {}).items(): regs.append((int(f), {"r": 0.95, **v}))
    err, sem = [], 0
    for f, v in regs:
        q = pj.get(str(f))
        if not q: sem += 1; continue
        js = q["r95"] if abs(v["r"] - 0.95) < 1e-6 else q["r10"]
        err.append(float(np.linalg.norm(np.array(js) - tpx(v["p"]))))
    out.append(f"{l} hélice (r = 10 cm e 95 cm): {len(err)} pares, erro máx. {max(err):.3f} px, médio {np.mean(err):.3f} px, sem quadro {sem}" if err else f"{l}: sem pares")
import sys
sys.path.insert(0, str(U))
from kit import projeta3d, cam_obl
pj = json.loads((U / "threejs/q3d/PT5_1920x1080/disco/pontos.json").read_text(encoding="utf-8")); ov = json.loads((U / "qa_overlay_PT5.json").read_text(encoding="utf-8"))
fs = sorted(int(k) for k in pj)
for f, v in ov.get("troca_2d3d", {}).items():
    k = min(fs, key=lambda x: abs(x - int(f)))
    out.append(f"PT5 troca disco 2D → 3D (quadro {k}): ponto de fora {np.linalg.norm(np.array(pj[str(k)]['P']) - tpx(v['p3'])):.3f} px, centro {np.linalg.norm(np.array(pj[str(k)]['centro']) - tpx(v['c'])):.3f} px")
er = [np.linalg.norm(np.array(pj[f]["vtopo"]) - tpx(v["vtopo"])) for f, v in ov.get("pv", {}).items() if f in pj and "vtopo" in pj[f]]
out.append(f"PT5 ponta de v⃗ = ω⃗ × r⃗: {len(er)} quadros, erro máx. {max(er):.3f} px" if er else "PT5 vtopo: sem pares")
pj = json.loads((U / "threejs/q3d/PE3_1920x1080/terra/pontos.json").read_text(encoding="utf-8")); ov = json.loads((U / "qa_overlay_PE3.json").read_text(encoding="utf-8"))
tvd = ov.get("terra_vet", {})
if tvd:
    v0 = list(tvd.values())[0]
    camG = cam_obl(-90.0, 16.0, (0.0, 0.0, 0.0), K=v0["K"], xc=v0["xc"], yc=v0["yc"], fov=16)
    f0 = min(int(k) for k in tvd)
    geo = [f for f, v in pj.items() if "SP" in v and v.get("vet") and int(f) >= f0]
    er = [np.linalg.norm(np.array(pj[f]["SP"]) - tpx(projeta3d(camG, np.array(pj[f]["vet"]["SP"])))) for f in geo]
    out.append(f"PE3 São Paulo (geo, {len(er)} quadros): erro máx. {max(er):.3f} px" if er else "PE3: sem quadros geo")
Path(U / "renders/v8/alinhamento_1080.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
