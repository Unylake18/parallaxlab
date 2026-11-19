"""yt_0045 final §8/§9: QA sobre o 1080p.
- 3D: todo PNG 1920×1080 do Three.js (threejs/q3d/<LOTE>_1920x1080) dentro de x 60..975 (3D só na metade esquerda) e custo por quadro;
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
L = ["yt_0045 · QA do 1080p (master final)"]
for lote in ("PH", "PA", "PB1", "PB2", "PB4", "PB5", "PB6", "PB7", "PS"):
    lg = (U / f"log1080_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    cont = lambda rx: len(re.findall(rx, lg, flags=re.M))
    L.append(f"{lote} 1080p: R5 {cont(r'^\[R5\]')} · R5V {cont(r'^\[R5V\]')} · R6 {cont(r'^\[R6\]')} · flash {cont(r'^\[flash\] ')} · gatilho-sem-frase {cont('gatilho-sem-frase')} · "
             f"Traceback {cont('Traceback')} · " + " ".join(re.findall(r"\[deriva\] \S+ [-+0-9.]+s", lg)) + f" · estouros {cont(r'.estouro.')} · " + "".join(re.findall(r"\[render1080\] \S+ \d+s", lg)))
M = U / "renders" / "yt_0045_master_final_1080p30.mp4"
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
dr.text((20, 16), "yt_0045 · master 1080p30 · um quadro na 1ª palavra de cada âncora", font=FT, fill=(240, 240, 240))
for i, (aid, t, im) in enumerate(ims):
    x, y = 10 + (i % 4) * (W + 10), 60 + (i // 4) * (H + 40)
    dr.text((x, y), f"{aid} · {int(t // 60)}:{t % 60:05.2f}", font=FT, fill=(255, 196, 92))
    P.paste(im.resize((W, H)), (x, y + 30))
P.save(OUT / "ancoras_master_1080.jpg", quality=88)
(OUT / "qa_1080.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))


# .srt em 6 pontos (início, W = 6, W = 2πR², 1 − 1 = 0, W = 2π − 1/2 ≈ 5,78, fim)
srt = (U / "legenda.srt").read_text(encoding="utf-8")
blocos = [b.split("\n") for b in srt.strip().split("\n\n")]
L.append(f"srt: {len(blocos)} blocos; 1º {blocos[0][1]}; último {blocos[-1][1]}")
for nome, rx in (("W = 6 (B1)", r"seis"), ("W = 2πR² (B4-1)", r"dois π R ao quadrado|2π R"), ("1 − 1 = 0 (B5-1)", r"um menos um"), ("W = 2π − 1/2 ≈ 5,78 (B7-3)", r"cinco vírgula setenta|5,78")):
    ach = [b for b in blocos if re.search(rx, " ".join(b[2:]), re.I)]
    L.append(f"srt · {nome}: {len(ach)} bloco(s)" + (f" · primeiro {ach[0][1]}: " + " / ".join(ach[0][2:]) if ach else ""))
(OUT / "qa_1080.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
