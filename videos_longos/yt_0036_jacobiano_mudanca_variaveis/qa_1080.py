"""yt_0036 final §8/§9 (copiado do yt_0034): QA sobre o 1080p.
- 3D: todo PNG 1920×1080 do Three.js (threejs/q3d/<LOTE>_1920x1080) sem alfa em y < 150 ou x > 1080 (canto e coluna) e custo por quadro;
- master: um quadro de cada âncora no instante da 1ª palavra (prancha) e o logo/canto presentes;
- A/V: duração do vídeo e do áudio, quadros, CRF gravado no stream.
Saídas: renders/final/qa_1080.txt e renders/final/ancoras_master_1080.jpg."""
import glob
import json
import re
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "final"
OUT.mkdir(parents=True, exist_ok=True)
L = ["yt_0036 · QA do 1080p (master final)"]
for lote in ("PB4",):
    fs = sorted(glob.glob(str(U / "threejs" / "q3d" / f"{lote}_1920x1080" / "*" / "*.png")))
    ruins, mx, my = 0, 0, 9999
    for f in fs:
        a = np.asarray(Image.open(f))[..., 3]
        cols = np.nonzero(a.max(0))[0]
        rows = np.nonzero(a.max(1))[0]
        if len(cols):
            mx, my = max(mx, cols.max()), min(my, rows.min())
            ruins += int(cols.max() > 1090 or rows.min() < 150)
    t = (U / f"tempo3d1080_{lote}.txt").read_text(encoding="utf-8", errors="replace").strip() if (U / f"tempo3d1080_{lote}.txt").exists() else ""
    L.append(f"3D {lote}: {len(fs)} PNG 1920×1080 · maior x {mx} px · menor y {my} px · fora do palco {ruins} · {t}")
M = U / "renders" / "yt_0036_master_final_1080p30.mp4"
c = av.open(str(M))
v, au = c.streams.video[0], c.streams.audio[0]
d = b"".join(bytes(p) for _, p in zip(range(4), c.demux(v)))
crf = re.search(rb"crf=([0-9.]+)", d).group(1).decode()
c.close()
c = av.open(str(M))
v = c.streams.video[0]
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
alvos = [(a, A["ancoras"][a]["ini"] + A["ancoras"][a]["t"][0]) for a in A["ordem"]]
ims, k, n = [], 0, 0
for fr in c.decode(v):
    t = float(fr.pts * v.time_base)
    n += 1
    while k < len(alvos) and t + 1 / 60 >= alvos[k][1]:
        ims.append((alvos[k][0], alvos[k][1], fr.to_image()))
        k += 1
dur_v = n / 30
c.close()
c = av.open(str(M))
dur_a = float(c.streams.audio[0].duration * c.streams.audio[0].time_base)
c.close()
L.append(f"master {M.name}: 1920×1080, {n} quadros a 30 fps = {dur_v:.2f} s; áudio {dur_a:.2f} s (WAV contínuo; a cauda de {dur_v - dur_a:.2f} s é o logo do CTA); crf={crf}")
logo = sum(1 for _, _, im in ims if np.asarray(im.crop((1640, 20, 1900, 110)).convert("L")).max() > 150)
L.append(f"prancha: {len(ims)} quadros (1ª palavra de cada âncora); logo presente em {logo}/{len(ims)}")
W, H = 640, 360
P = Image.new("RGB", (4 * W + 50, ((len(ims) + 3) // 4) * (H + 40) + 60), (22, 18, 34))
dr = ImageDraw.Draw(P)
try:
    FT = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
except OSError:
    FT = ImageFont.load_default()
dr.text((20, 16), "yt_0036 · master 1080p30 · um quadro na 1ª palavra de cada âncora", font=FT, fill=(240, 240, 240))
for i, (aid, t, im) in enumerate(ims):
    x, y = 10 + (i % 4) * (W + 10), 60 + (i // 4) * (H + 40)
    dr.text((x, y), f"{aid} · {int(t // 60)}:{t % 60:05.2f}", font=FT, fill=(255, 196, 92))
    P.paste(im.resize((W, H)), (x, y + 30))
P.save(OUT / "ancoras_master_1080.jpg", quality=88)
(OUT / "qa_1080.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))

# alinhamento 3D × Manim no 1080p30: rótulos presos (renders/v1/qa/al/<LOTE>.json, gravado pelo último render, aqui o de 1080p) × pontos.json do
# three.js em 1920×1080 no mesmo quadro
L2 = []
for l in ("PB4",):
    a = U / "renders" / "final" / "qa" / "al" / f"{l}.json"
    al = json.loads(a.read_text(encoding="utf-8"))
    cache, pior, n, falta = {}, 0.0, 0, 0
    for _, cena, fq, nome, x, y in al:
        if cena not in cache:
            pj = U / "threejs" / "q3d" / f"{l}_1920x1080" / cena / "pontos.json"
            cache[cena] = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
        p = cache[cena].get(str(fq), {}).get(nome)
        if p is None:
            falta += 1
            continue
        n += 1
        pior = max(pior, float(np.hypot(p[0] - x, p[1] - y)))
    L2.append(f"alinhamento 1080p {l}: {n} medidas, pior {pior:.2f} px; sem par {falta}")
(OUT / "qa_1080.txt").write_text("\n".join(L + L2) + "\n", encoding="utf-8")
print("\n".join(L2))
