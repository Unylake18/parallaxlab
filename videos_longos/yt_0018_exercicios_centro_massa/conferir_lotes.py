"""yt_0018 v7: confere que cada lote renderizado tem exatamente os quadros que a voz manda (janelas de ancoras.json) e o atraso de abertura de cada âncora.
uso: python conferir_lotes.py"""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem, A = ANC["ordem"], ANC["ancoras"]
LOTES = {"PH": ("H1", "A4"), "PX0": ("X0-1", "X1-4"), "PX2": ("X2-1", "X2-4"), "PX3": ("X3-1", "X3-10"), "PX4": ("X4-1", "X4-5"), "PX5": ("X5-1", "X5-8"),
         "PEP": ("EP1", "EN2")}
tot = 0
for l, (a0, a1) in LOTES.items():
    ini, fim = A[a0]["ini"], A[a1]["fim"]
    esperado = round((fim - ini) * 15)
    t = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") if (U / f"log_{l}.txt").exists() else ""
    m = re.search(r"\[tempo\] total [0-9.]+ s \((\d+) quadros\)", t)
    real = int(m.group(1)) if m else None
    ab = re.findall(r"\[abertura\] (\S+) atrasada ([-+0-9.]+) s", t)
    print(f"{l:4s} {a0}…{a1}: esperado {esperado} quadros ({fim - ini:.2f} s), real {real}" + ("  OK" if real == esperado else f"  DIFERENÇA {None if real is None else real - esperado}") + (f"  aberturas atrasadas: {ab}" if ab else ""))
