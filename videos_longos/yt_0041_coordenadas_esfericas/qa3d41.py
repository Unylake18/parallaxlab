"""yt_0041 · QA do 3D (handoff v4 §3): (2) pixels do 3D fora de x = 60..975 e (7) G1–G6 por cena + prancha 2×3 por lote.
Saídas em renders/v4/qa/: tela3d_v5.txt, tamanhos_v5.txt, pranchas3d/<LOTE>_2x3.jpg."""
import os
import glob, re, sys
from pathlib import Path
import numpy as np
from PIL import Image
AQUI = Path(__file__).resolve().parent
QA = AQUI / "renders" / os.environ.get("RODADA", "v5") / "qa"
QA.mkdir(parents=True, exist_ok=True)
(QA / "pranchas3d").mkdir(exist_ok=True)
LOTES = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
out = ["3D: PIXELS FORA DE x = 60..975 (px de 1080p; amostra de até 60 quadros por cena; alfa > 12)", "",
       f"{'lote':5} {'cena':10} {'x min':>6} {'x max':>6} {'y min':>6} {'y max':>6}  nota"]
for L in LOTES:
    for d in sorted(glob.glob(str(AQUI / "threejs" / "q3d" / f"{L}_960x540" / "*"))):
        d = Path(d)
        fs = sorted(d.glob("f*.png"))
        if not fs:
            continue
        passo = max(1, len(fs) // 60)
        x0 = y0 = 1e9
        x1 = y1 = -1
        for f in fs[::passo]:
            a = np.array(Image.open(f).convert("RGBA"))[..., 3]
            ys, xs = np.nonzero(a > 12)
            if len(xs):
                x0, x1 = min(x0, xs.min() * 2), max(x1, xs.max() * 2)
                y0, y1 = min(y0, ys.min() * 2), max(y1, ys.max() * 2)
        par = d.name in ("caixa", "bolagrade")
        nota = "duas peças lado a lado (B1-3/B3-1): regra x ≤ 975 não se aplica" if par and x1 > 975 else ("OK" if (x0 >= 56 and x1 <= 979) else "FORA")
        out.append(f"{L:5} {d.name:10} {int(x0):6} {int(x1):6} {int(y0):6} {int(y1):6}  {nota}")
(QA / "tela3d_v5.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
# tamanhos (KaTeX px pedidos no código por arquivo)
tam = ["TAMANHOS PEDIDOS NO CÓDIGO (KaTeX px; L/TC/mixl/chip), por seção — menor e maior; fórmula principal ≥ 44, nada < 26", ""]
for f in sorted(AQUI.glob("sec_*.py")):
    t = f.read_text(encoding="utf-8")
    vs = [int(m.group(1)) for m in re.finditer(r"\], \d+, \d+, (\d+)(?:, \"[lcr]\")?\)", t)]
    vs += [int(m.group(1)) for m in re.finditer(r"(?:TC|tc|rotP)\(.*?, (\d+)(?:, \"[lcr]\")?\)$", t, re.M)]
    if vs:
        tam.append(f"{f.name:12} n={len(vs):3d}  min={min(vs)}  max={max(vs)}  < 36: {sum(v < 36 for v in vs)}")
(QA / "tamanhos_v5.txt").write_text("\n".join(tam), encoding="utf-8")
print("\n".join(tam))
# pranchas 2×3 por lote (6 quadros igualmente espaçados do render do lote)
import av
for L in LOTES:
    mp4 = AQUI / f"media_{L}" / "videos" / "cena" / "540p15" / f"{L}.mp4"
    if not mp4.exists():
        continue
    c = av.open(str(mp4))
    st = c.streams.video[0]
    n = st.frames
    alvo = [int(n * (k + .5) / 6) for k in range(6)]
    ims = {}
    for i, fr in enumerate(c.decode(st)):
        if i in alvo:
            ims[i] = fr.to_image()
        if i >= max(alvo):
            break
    c.close()
    pr = Image.new("RGB", (960 * 3, 540 * 2))
    for k, q in enumerate(alvo):
        if q in ims:
            pr.paste(ims[q], ((k % 3) * 960, (k // 3) * 540))
    pr.resize((1920 * 3 // 4, 1080 * 3 // 4 // 1)).save(QA / "pranchas3d" / f"{L}_2x3.jpg", quality=85)
print("pranchas ok")
