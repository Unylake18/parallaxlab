"""v4 §10.4: comparações v3 × v4 no mesmo ponto da fala (âncora + fração; âncoras do v3 em _v3/logs/, do v4 nos logs atuais).
1. os 13 casos da §2 antes (preview v3) e depois (preview v4) → renders/v4/casos_antes_depois.png e renders/v4/casos/caso_NN_{antes,depois}.png
2. o lago v3 × v4 (hook e X3) → renders/v4/lago_v3_x_v4.png
3. três quadros do X3 em cada enquadramento (PERTO e LONGE) → renders/v4/x3_perto_longe.png
uso: python comparar_v4.py"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
from casos13 import CASOS  # noqa: E402

ini3 = json.loads((U / "renders" / "v3" / "inicio_lotes.json").read_text(encoding="utf-8"))
ini4 = json.loads((U / "renders" / "v4" / "inicio_lotes.json").read_text(encoding="utf-8"))
P3V = U / "renders" / "preview_yt0018_v3_960x540.mp4"
P4V = U / "renders" / "preview_yt0018_v4_960x540.mp4"


def anc(f):
    a = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", f.read_text(encoding="utf-8", errors="replace"))]
    return a, {x: (t, a[i + 1][1] if i + 1 < len(a) else t + 10) for i, (x, t) in enumerate(a)}


def v3_para_v4(lote, t_prev3):
    """Tempo no preview v3 → (quadro v3, quadro v4, âncora, fração)."""
    tl = t_prev3 - ini3[lote]
    lista3, _ = anc(U / "_v3" / "logs" / f"log_{lote}.txt")
    _, d4 = anc(U / f"log_{lote}.txt")
    k = max([i for i, (a, t) in enumerate(lista3) if t <= tl + 1e-6] or [0])
    aid, t0 = lista3[k]
    t1 = lista3[k + 1][1] if k + 1 < len(lista3) else t0 + 5
    fr = (tl - t0) / max(t1 - t0, 1e-6)
    s4, e4 = d4.get(aid, (0.0, 1.0))
    return int(round(t_prev3 * 15)), int(round((ini4[lote] + s4 + fr * (e4 - s4)) * 15)), aid, fr


def quadros(arq, qs):
    c = av.open(str(arq))
    out, mx = {}, max(qs)
    for i, f in enumerate(c.decode(video=0)):
        if i in qs:
            out[i] = f.to_image()
        if i > mx:
            break
    c.close()
    return out


def prancha(pares, rot_a, rot_b, saida, pasta=None):
    a = quadros(P3V, {p[0] for p in pares})
    b = quadros(P4V, {p[1] for p in pares})
    W, H = 640, 360
    pr = Image.new("RGB", (2 * W + 10, len(pares) * (H + 22)), "black")
    d = ImageDraw.Draw(pr)
    for k, (q3, q4, nome) in enumerate(pares):
        y = k * (H + 22)
        pr.paste(a[q3].resize((W, H)), (0, y + 22))
        pr.paste(b[q4].resize((W, H)), (W + 10, y + 22))
        d.text((4, y + 5), f"{rot_a} {q3 / 15 // 60:.0f}:{q3 / 15 % 60:04.1f} · {nome}", fill="yellow")
        d.text((W + 14, y + 5), f"{rot_b} {q4 / 15 // 60:.0f}:{q4 / 15 % 60:04.1f}", fill="yellow")
        if pasta is not None:
            a[q3].save(pasta / f"caso_{k + 1:02d}_antes.png")
            b[q4].save(pasta / f"caso_{k + 1:02d}_depois.png")
    pr.save(saida)


# 1. os 13 casos
pares = []
for n, (t0, t1), lote, _, desc in CASOS:
    q3, q4, aid, fr = v3_para_v4(lote, t0 if t1 - t0 < 0.05 else t0 + 0.4 * (t1 - t0))
    pares.append((q3, q4, f"#{n} ({aid} {fr:.2f}) {desc}"))
(U / "renders" / "v4" / "casos").mkdir(parents=True, exist_ok=True)
prancha(pares, "ANTES v3", "DEPOIS v4", U / "renders" / "v4" / "casos_antes_depois.png", U / "renders" / "v4" / "casos")
# 2. o lago v3 × v4 (hook e X3)
EST = [("PH", "H1", 0.4, "H1 lago (água)"), ("PH", "H1", 0.9, "H1 coluna da lua"), ("PH", "H2", 0.85, "H2 replay de lado"),
       ("PX3", "X3-1", 0.6, "X3-1 dados"), ("PX3", "X3-5", 0.55, "X3-5 voo"), ("PX3", "X3-7", 0.5, "X3-7 quase vertical")]
_, d3 = {}, {}
pares = []
for lote, aid, fr, nome in EST:
    _, a3 = anc(U / "_v3" / "logs" / f"log_{lote}.txt")
    _, a4 = anc(U / f"log_{lote}.txt")
    s3, e3 = a3[aid]
    s4, e4 = a4[aid]
    pares.append((int(round((ini3[lote] + s3 + fr * (e3 - s3)) * 15)), int(round((ini4[lote] + s4 + fr * (e4 - s4)) * 15)), nome))
prancha(pares, "v3", "v4", U / "renders" / "v4" / "lago_v3_x_v4.png")
# 3. X3: três quadros PERTO e três LONGE (vista registrada no pedido 3D: K da câmera)
ped = json.loads((U / "threejs" / "pedidos3d" / "PX3.json").read_text(encoding="utf-8"))["cenas"]["lago"]
perto = [f for f, e in ped if e["cam"]["K"] > 15.0]
longe = [f for f, e in ped if e["cam"]["K"] < 5.3]
esc = lambda L: [L[int(len(L) * u)] for u in (0.15, 0.5, 0.85)] if L else []
qs = esc(perto) + esc(longe)
im = quadros(U / "media_PX3/videos/cena/540p15/PX3.mp4", set(qs))
W, H = 640, 360
pr = Image.new("RGB", (2 * W + 10, 3 * (H + 22)), "black")
d = ImageDraw.Draw(pr)
for k, (a, b) in enumerate(zip(esc(perto), esc(longe))):
    y = k * (H + 22)
    pr.paste(im[a].resize((W, H)), (0, y + 22))
    pr.paste(im[b].resize((W, H)), (W + 10, y + 22))
    d.text((4, y + 5), f"PERTO · X3 {a / 15:.1f} s (preview {(ini4['PX3'] + a / 15) // 60:.0f}:{(ini4['PX3'] + a / 15) % 60:04.1f})", fill="yellow")
    d.text((W + 14, y + 5), f"LONGE ÷3 · X3 {b / 15:.1f} s (preview {(ini4['PX3'] + b / 15) // 60:.0f}:{(ini4['PX3'] + b / 15) % 60:04.1f})", fill="yellow")
pr.save(U / "renders" / "v4" / "x3_perto_longe.png")
print("ok")
