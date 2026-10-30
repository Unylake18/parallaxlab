"""Stills 1920×1080 do v4 (handoff v4 §5) → renders/stills_v4/. Instante = início da âncora + fração × duração real (lida do [ancora] em log_<lote>.txt).
Lotes com fundo 3D: o r3d.js renderiza em 1920×1080 só os quadros perto do instante (a partir dos pedidos da passagem seca).
uso: python stills_v4.py [nome ...]"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PY = r"C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
NODE_PATH = str((AQUI.parent / "yt_0015_momento_impulso" / "threejs" / "node_modules").resolve())
STILLS = [  # nome, lote, âncora, fração, 3D?
    ("H2_balancim_T_e_menos_T", "PH", "H2", 0.6, True),
    ("A2_miniatura_parada", "PH", "A2", 0.8, True),
    ("T7-3_soma_em_tres_linhas", "P7", "T7-3", 0.5, True),
    ("T8-4_conta_e_2608N", "P8", "T8-5", 0.97, True),
    ("T8-6_firme_x_gelo", "P8", "T8-6", 0.95, True),
    ("T9-7_graficos_completos", "P9", "T9-7", 0.9, False),
    ("T10_fim_texto_BODY", "P10", "T10-3", 0.95, False),
    ("E6-3_rebate", "Q6", "E6-3", 0.95, True),
    ("E7-4_px_por_cima_da_cabeca", "Q7", "E7-4", 0.525, True),
    ("E8-4_setas_e_DICA", "Q8", "E8-4", 0.9, False),
    ("C-1_luz_placas", "PC", "C-1", 0.92, False),
    ("RESUMO_ideia_3", "PS", "S2", 0.95, True),
]


def instante(lote, aid, frac):
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8"))]
    for (a, t0), (_, t1) in zip(an, an[1:]):
        if a == aid:
            return t0 + frac * (t1 - t0)
    raise KeyError(aid)


os.makedirs(AQUI / "renders" / "stills_v4", exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING="utf-8", NODE_PATH=NODE_PATH, CHROMIUM_PATH=r"C:/Program Files/Google/Chrome/Application/chrome.exe")
pedir = set(sys.argv[1:])
for nome, lote, aid, frac, tem3d in STILLS:
    if pedir and nome not in pedir:
        continue
    T = instante(lote, aid, frac)
    f = int(round(T * 15))
    if tem3d:
        ped = json.loads((AQUI / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))
        extra = range(350, 380) if nome.startswith("A2") else ()     # o A2 mostra a miniatura do último quadro do hook
        so = ",".join(str(q) for q in [*range(max(0, f - 2), f + 50), *extra])
        subprocess.run(["node", "r3d.js", "--lote", lote, "--w", "1920", "--h", "1080", "--so", so], cwd=AQUI / "threejs", env=env,
                       stdout=subprocess.DEVNULL, check=True)
    md = AQUI / f"media_still_{lote}"
    subprocess.run([PY, "-m", "manim", "-r", "1920,1080", "--fps", "15", "--progress_bar", "none", "-s", "cena.py", lote], cwd=AQUI,
                   env=dict(env, MEDIA_DIR=str(md), STILL=str(T)), stdout=open(AQUI / f"log_still_{lote}.txt", "w"), stderr=subprocess.STDOUT)
    png = max(md.rglob(f"{lote}*.png"), key=lambda p: p.stat().st_mtime)
    shutil.copy(png, AQUI / "renders" / "stills_v4" / f"{nome}.png")
    print(f"{nome}.png @ {T:.2f} s")
