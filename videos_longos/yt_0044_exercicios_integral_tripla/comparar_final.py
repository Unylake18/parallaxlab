"""yt_0044 final: junta os stills 1080p nativos (renders/still/LOTE_T.png, T = marca − 0,02 s) com os alvos v2 → renders/final/qa/comparacao_v2/NN_*.jpg (still | alvo) e stills/NN_*.png."""
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "final" / "qa" / "comparacao_v2"
(OUT / "stills").mkdir(parents=True, exist_ok=True)
n = 0
for L in ["PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"]:
    for m in re.finditer(r"^\[marca\] (\S+) ([0-9.]+)", (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace"), flags=re.M):
        alvo, t = m.group(1), float(m.group(2))
        st = U / "renders" / "still" / f"{L}_{t - 0.02:.3f}.png"
        al = next((U / "referencia" / "yt_0044_quadros_alvo_v2").glob(f"{alvo}_*.jpg"), None)
        if not st.exists() or al is None:
            print("FALTA", L, alvo, st.name, al)
            continue
        a, b = Image.open(st).convert("RGB"), Image.open(al).convert("RGB").resize((1920, 1080))
        c = Image.new("RGB", (3840, 1080)); c.paste(a, (0, 0)); c.paste(b, (1920, 0))
        ImageDraw.Draw(c).rectangle([1916, 0, 1923, 1079], fill=(255, 255, 255))
        c.save(OUT / f"{alvo}.jpg", quality=92); shutil.copy(st, OUT / "stills" / f"{alvo}.png"); n += 1
print(n, "pares")
