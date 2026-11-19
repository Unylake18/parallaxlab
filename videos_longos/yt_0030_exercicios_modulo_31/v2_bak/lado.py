"""Conferência rápida: alvo (em cima, 960×540) × still do render (embaixo). uso: python lado.py PH_33 03 → renders/still/cmp_PH_33.png"""
import sys
from pathlib import Path
from PIL import Image
U = Path(__file__).resolve().parent
r = Image.open(U / "renders/still" / f"{sys.argv[1]}.png").convert("RGB")
a = Image.open(next((U / "referencia_v1").glob(f"{sys.argv[2]}_*.jpg"))).convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.new("RGB", (960, 1084), (255, 255, 255))
o.paste(a, (0, 0)); o.paste(r, (0, 544))
o.save(U / "renders/still" / f"cmp_{sys.argv[1]}.png")
