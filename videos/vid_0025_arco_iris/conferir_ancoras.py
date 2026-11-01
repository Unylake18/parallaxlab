"""Prancha de conferência do vid_0025: o quadro do vídeo 0,25 s depois do início de cada palavra-âncora, com a frase falada.
Uso: conferir_ancoras.py VIDEO PREFIXO_SAIDA   (usa sync.json: T = instante da palavra no vídeo)"""
import json, sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent
V, PRE = sys.argv[1], sys.argv[2]
sy = json.loads((PASTA / "sync.json").read_text(encoding="utf-8"))
an = json.loads((PASTA / "ancoras.json").read_text(encoding="utf-8"))
pal = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
fonte = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
c = av.open(V); st = c.streams.video[0]
frames = [fr.to_image().convert("RGB") for fr in c.decode(st)]
fps = float(st.average_rate)
nomes = [n for n in sy["order"] if n != "fim"]
imgs = []
for n in nomes:
    t = sy["T"][n] + 0.25
    im = frames[min(int(round(t * fps)), len(frames) - 1)].copy().resize((270, 480))
    i = next((k for k, p in enumerate(pal) if abs(p["start"] - an["A"][n]) < 1e-6), 0)
    fala = " ".join(p["word"] for p in pal[i:i + 5])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 438, 270, 480], fill=(0, 0, 0))
    d.text((4, 440), f"{n}  T={sy['T'][n]:.2f}s", fill=(120, 230, 255), font=fonte)
    d.text((4, 460), fala.encode("latin-1", "replace").decode("latin-1")[:34], fill=(255, 255, 255), font=fonte)
    imgs.append(im)
for g in range(0, len(imgs), 12):
    lote = imgs[g:g + 12]
    folha = Image.new("RGB", (270 * 6 + 10, 480 * 2 + 4), (25, 25, 35))
    for i, im in enumerate(lote):
        folha.paste(im, (2 + (i % 6) * 272, 2 + (i // 6) * 482))
    folha.save(f"{PRE}_{g // 12 + 1:02d}.png")
print(len(imgs), "âncoras;", (len(imgs) + 11) // 12, "pranchas")
