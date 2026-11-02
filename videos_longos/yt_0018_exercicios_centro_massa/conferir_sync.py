"""yt_0018 v7: prancha de sincronia — o quadro do vídeo no INÍCIO de cada frase da narração, com a frase escrita embaixo e o instante.
Cada frase vem de narracao_tags_v1_4.md (Texto corrido), o instante da primeira palavra vem de audio/voz7_tempos.json (alinhamento da voz contínua)
e o quadro vem do preview com voz. Quem olha confere se a imagem do início da frase é a da frase.
Grava renders/v7/sync/prancha_sync_NN.png (20 quadros por prancha) e renders/v7/sync/frases.json.
uso: python conferir_sync.py [video]"""
import json
import re
import sys
import textwrap
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
VID = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "preview_yt0018_v7_960x540.mp4"
OUT = U / "renders" / "v7" / "sync"
OUT.mkdir(parents=True, exist_ok=True)
T = json.loads((U / "audio" / "voz7_tempos.json").read_text(encoding="utf-8"))["ancoras"]
ordem = json.loads((U / "ancoras_nominal.json").read_text(encoding="utf-8"))["ordem"]
texto = (U / "narracao_tags_v1_4.md").read_text(encoding="utf-8")
corpo = texto[texto.index("## Texto corrido (para gravação)"):].split("\n", 1)[1]
linhas = [l.strip() for l in corpo.splitlines() if l.strip()]

frases = []
for aid, linha in zip(ordem, linhas):
    limpo = re.sub(r"\[[^\]]*\]", "", linha).replace("**", "")
    limpo = " ".join(limpo.split())
    k = 0
    for sent in re.split(r"(?<=[.!?…])\s+", limpo):
        n = len(re.findall(r"\w+", sent))
        if n == 0:
            continue
        if k < len(T[aid]):
            frases.append({"aid": aid, "t": T[aid][k]["t"], "frase": sent})
        k += n
quer = {int(round(f["t"] * 15)): f for f in frases}
ims = {}
c = av.open(str(VID))
for i, fr in enumerate(c.decode(video=0)):
    if i in quer:
        ims[i] = fr.to_image()
    if i >= max(quer):
        break
c.close()
W, H, CAP, COLS, LIN = 480, 270, 62, 4, 5
try:
    fonte = ImageFont.truetype("arial.ttf", 13)
except Exception:
    fonte = ImageFont.load_default()
por = COLS * LIN
for pg in range((len(frases) + por - 1) // por):
    lote = frases[pg * por:(pg + 1) * por]
    pr = Image.new("RGB", (COLS * W, LIN * (H + CAP)), "black")
    d = ImageDraw.Draw(pr)
    for j, f in enumerate(lote):
        x, y = (j % COLS) * W, (j // COLS) * (H + CAP)
        q = int(round(f["t"] * 15))
        if q in ims:
            pr.paste(ims[q].resize((W, H)), (x, y))
        d.rectangle([x, y + H, x + W - 1, y + H + CAP - 1], fill=(14, 20, 40))
        mm, ss = divmod(f["t"], 60)
        d.text((x + 4, y + H + 2), f"{int(mm)}:{ss:05.2f}  {f['aid']}", fill="yellow", font=fonte)
        d.text((x + 4, y + H + 18), "\n".join(textwrap.wrap(f["frase"], 70)[:3]), fill="white", font=fonte)
    pr.save(OUT / f"prancha_sync_{pg + 1:02d}.png")
(OUT / "frases.json").write_text(json.dumps(frases, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(frases)} frases; {(len(frases) + por - 1) // por} pranchas em {OUT}")
