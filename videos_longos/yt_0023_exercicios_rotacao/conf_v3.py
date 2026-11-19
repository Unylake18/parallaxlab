import json
from pathlib import Path
import av
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
Q = json.loads((U / "renders/quadros_v3.json").read_text(encoding="utf-8"))
ini = sorted(Q.values())
def quadro(a, fr):
    i0 = Q[a]; i1 = min(v for v in ini if v > i0)
    return int(i0 + fr * (i1 - i0))
PEDE = [("E3-1_geral", "E3-1", 0.02), ("E3-1_perfil", "E3-1", 0.2), ("E3-1_explodido", "E3-1", 0.45), ("E3-1_close", "E3-1", 0.75), ("E3-1_volta", "E3-1", 0.97),
        ("E3-3", "E3-3", 0.5), ("E3-7", "E3-7", 0.6), ("E1-1_anel", "E1-1", 0.22), ("E1-1_cubo", "E1-1", 0.42), ("E1-1_discos", "E1-1", 0.6),
        ("E1-1_tambor", "E1-1", 0.78), ("E1-1_bloco", "E1-1", 0.92), ("E1-3_corte", "E1-3", 0.2), ("E1-3_cotas", "E1-3", 0.45), ("E1-4_cubo", "E1-4", 0.35),
        ("E1-4_disco", "E1-4", 0.8), ("E1-5_explodido", "E1-5", 0.15), ("E1-5_voo", "E1-5", 0.3), ("E1-6", "E1-6", 0.5), ("E1-9", "E1-9", 0.7)]
alvo = {}
for n, a, fr in PEDE: alvo.setdefault(quadro(a, fr), []).append(n)
od = U / "renders/conferencia_v3"; od.mkdir(parents=True, exist_ok=True)
c = av.open(str(U / "renders/preview_yt0023_v3_960x540.mp4"))
ims = []
for i, f in enumerate(c.decode(video=0)):
    if i in alvo:
        im = f.to_image()
        for n in alvo[i]:
            im.save(od / f"{n}.png"); d = im.copy(); ImageDraw.Draw(d).text((6, 4), n, fill=(255, 255, 0)); ims.append((n, d))
    if i > max(alvo): break
ims.sort(key=lambda t: [p[0] for p in PEDE].index(t[0]))
cols = 4; rows = (len(ims) + cols - 1) // cols
pr = Image.new("RGB", (480 * cols, 270 * rows))
for k, (n, im) in enumerate(ims): pr.paste(im.resize((480, 270)), ((k % cols) * 480, (k // cols) * 270))
pr.save(U / "renders/prancha_conferencia_v3.png"); print(len(ims), "quadros")
