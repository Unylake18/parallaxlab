"""Extrai quadros de um lote renderizado (media_<LOTE>/videos/cena/540p15/<LOTE>.mp4) nos instantes dados (s do lote) e monta uma prancha.
uso: python quadros.py PH 10 30.5 52.2 [--alvo 01_H1_bola_pesada_trava.jpg]  → renders/v1/qa/q/<LOTE>_<t>.png e prancha <LOTE>_q.jpg"""
import sys
from pathlib import Path
import av
from PIL import Image
AQUI = Path(__file__).resolve().parent
lote = sys.argv[1]
ts = [float(x) for x in sys.argv[2:] if not x.startswith("--") and not x.endswith(".jpg")]
alvo = next((x for x in sys.argv[2:] if x.endswith(".jpg")), None)
arq = AQUI / f"media_{lote}" / "videos" / "cena" / "540p15" / f"{lote}.mp4"
out = AQUI / "renders" / "v3" / "qa" / "q"
out.mkdir(parents=True, exist_ok=True)
c = av.open(str(arq))
st = c.streams.video[0]
fps = float(st.average_rate)
alvos = sorted(int(round(t * fps)) for t in ts)
ims, i, k = {}, 0, 0
for fr in c.decode(st):
    while k < len(alvos) and i == alvos[k]:
        ims[alvos[k]] = fr.to_image()
        k += 1
    i += 1
    if k >= len(alvos):
        break
fs = []
for q in alvos:
    p = out / f"{lote}_{q / fps:.2f}.png"
    ims[q].save(p)
    fs.append(ims[q])
if alvo:
    fs.append(Image.open(AQUI / "referencia" / "yt_0041_quadros_alvo_v1_1" / alvo).resize((960, 540)))
n = len(fs)
cols = 2
rows = (n + 1) // 2
pr = Image.new("RGB", (960 * cols, 540 * rows), (0, 0, 0))
for j, im in enumerate(fs):
    pr.paste(im.convert("RGB"), ((j % cols) * 960, (j // cols) * 540))
pr.save(out / f"{lote}_q.jpg", quality=90)
print("ok", [round(q / fps, 2) for q in alvos], "→", out / f"{lote}_q.jpg")
