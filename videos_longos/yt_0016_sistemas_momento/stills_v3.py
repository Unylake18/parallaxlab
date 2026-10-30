"""Stills 1920×1080 do v3 (handoff v3 §5) → renders/stills_v3/. Instante = início da âncora + fração × duração real (lida do [ancora] em log_<lote>.txt).
Lotes com fundo 3D: o r3d.js renderiza em 1920×1080 só os quadros perto do instante (a partir dos pedidos da passagem seca).
uso: python stills_v3.py [nome ...]"""
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
    ("H1_setas_arreio_e_pedra", "PH", "H1", 0.9, True),
    ("T8-4_conta_e_setas", "P8", "T8-4", 0.97, True),
    ("T8-5_2608N_fora_da_cabeca", "P8", "T8-5", 0.97, True),
    ("T8-6_gelo", "P8", "T8-6", 0.95, True),
    ("T9-7_graficos_empilhados", "P9", "T9-7", 0.55, False),
    ("T10_fim_texto_aprovado", "P10", "T10-3", 0.95, False),
    ("E7-4_normal_px_py", "Q7", "E7-4", 0.8, True),
    ("E7-5_barras_na_conta", "Q7", "E7-5", 0.78, True),
    ("RESUMO_tres_ideias", "PS", "S2", 0.97, True),
]


def instante(lote, aid, frac):
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8"))]
    for (a, t0), (_, t1) in zip(an, an[1:]):
        if a == aid:
            return t0 + frac * (t1 - t0)
    raise KeyError(aid)


os.makedirs(AQUI / "renders" / "stills_v3", exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING="utf-8", NODE_PATH=NODE_PATH, CHROMIUM_PATH=r"C:/Program Files/Google/Chrome/Application/chrome.exe")
pedir = set(sys.argv[1:])
for nome, lote, aid, frac, tem3d in STILLS:
    if pedir and nome not in pedir:
        continue
    T = instante(lote, aid, frac)
    f = int(round(T * 15))
    if tem3d:
        ped = json.loads((AQUI / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))
        so = ",".join(str(q) for q in range(max(0, f - 2), f + 50))
        subprocess.run(["node", "r3d.js", "--lote", lote, "--w", "1920", "--h", "1080", "--so", so], cwd=AQUI / "threejs", env=env,
                       stdout=subprocess.DEVNULL, check=True)
    md = AQUI / f"media_still_{lote}"
    subprocess.run([PY, "-m", "manim", "-r", "1920,1080", "--fps", "15", "--progress_bar", "none", "-s", "cena.py", lote], cwd=AQUI,
                   env=dict(env, MEDIA_DIR=str(md), STILL=str(T)), stdout=open(AQUI / f"log_still_{lote}.txt", "w"), stderr=subprocess.STDOUT)
    png = max(md.rglob(f"{lote}*.png"), key=lambda p: p.stat().st_mtime)
    shutil.copy(png, AQUI / "renders" / "stills_v3" / f"{nome}.png")
    print(f"{nome}.png @ {T:.2f} s")
