"""yt_0045 · comparação still × alvo em resolução cheia (§1, §8.1 item 13).
uso: python compara.py LOTE T NN_ALVO.jpg   (still nativo 1920×1080 em renders/still/LOTE_T.png, do ./still.sh LOTE T)
Saída: renders/v3/qa/comparacao/NN_<cena>.jpg = still (esquerda) | alvo v3 (direita), 3840×1080, e o still sozinho em .../stills/NN_<cena>.png."""
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
lote, t, alvo = sys.argv[1], sys.argv[2], sys.argv[3]
st = AQUI / "renders" / "still" / f"{lote}_{t}.png"
al = AQUI / "referencia" / "quadros_alvo_v3" / alvo
out = AQUI / "renders" / os.environ.get("RODADA", "v3") / "qa" / "comparacao"
(out / "stills").mkdir(parents=True, exist_ok=True)
a = Image.open(st).convert("RGB")
b = Image.open(al).convert("RGB")
assert a.size == (1920, 1080), a.size
c = Image.new("RGB", (3840, 1080))
c.paste(a, (0, 0))
c.paste(b.resize((1920, 1080)), (1920, 0))
d = ImageDraw.Draw(c)
d.rectangle([1916, 0, 1923, 1079], fill=(255, 255, 255))
nome = alvo.rsplit(".", 1)[0]
c.save(out / f"{nome}.jpg", quality=92)
shutil.copy(st, out / "stills" / f"{nome}.png")
print("ok", out / f"{nome}.jpg")
