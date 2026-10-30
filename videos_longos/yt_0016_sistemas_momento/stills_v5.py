"""Stills 1920×1080 das correções do v5 (handoff v5 §5: V3, V7, V12–V14, V17, e as mudanças de física) → renders/stills_v5/.
Instante = quando a voz diz a frase (ancoras.json) + atraso, no relógio do lote (o lote começa na sua primeira âncora).
Lotes com fundo 3D: o r3d.js renderiza em 1920×1080 só os quadros perto do instante (a partir dos pedidos da passagem seca).
uso: python stills_v5.py [nome ...]"""
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PY = r"C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
NODE_PATH = str((AQUI.parent / "yt_0015_momento_impulso" / "threejs" / "node_modules").resolve())
PRIMEIRA = {"PH": "H1", "P7": "T7-1", "P8": "T8-1", "P9": "T9-1", "P10": "T10-1", "Q6": "E6-1", "Q7": "E7-1", "Q8": "E8-1", "Q9": "E9-1",
            "PC": "C-1", "PS": "S1"}
STILLS = [  # nome, lote, âncora, frase, atraso (s), 3D?
    ("V3_T7-3_risco_e_troca", "P7", "T7-3", "Sobra só a força externa", 1.3, True),
    ("V7_T8-8_rotulos_do_pe", "P8", "T8-8", "e o atrito do chão", 1.0, True),
    ("V12_E7-3_camera_lenta_e_lago", "Q7", "E7-3", "A bala leva momento para cima", 0.4, True),
    ("V13_E7-3_normal_e_recuo", "Q7", "E7-3", "Então quem segurou ele", 0.9, True),
    ("V14_E7-4_X_em_py", "Q7", "E7-4", "Mas na horizontal", 1.2, True),
    ("V17_C-1_placas_e_conta", "PC", "C-1", "Por isso o espelho", 1.0, False),
    ("F_T8-6_coeficiente_cinetico", "P8", "T8-6", "Olha as barras", 1.6, True),
    ("F_T8-7_peso_externo", "P8", "T8-7", "A Lua vai ter que esperar", 0.4, False),
    ("F_T10-1_antes_dos_batentes", "P10", "T10-1", "Mas as energias", 0.8, False),
    ("F_E7-5_coice", "Q7", "E7-5", "A força do recuo", 1.0, True),
    ("F_S2_quem_ficou_de_fora", "PS", "S2", "procure as forças externas", 0.5, True),
]
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and c.isalnum())


def instante(lote, aid, frase, dt):
    alvo = [norm(w) for w in frase.split()]
    pal = ANC[aid]["palavras"]
    ws = [w for w, _ in pal]
    for i in range(len(ws) - len(alvo) + 1):
        if ws[i:i + len(alvo)] == alvo:
            return round((pal[i][1] + dt) * 15) / 15 - round(ANC[PRIMEIRA[lote]]["t0"] * 15) / 15
    raise KeyError((aid, frase))


os.makedirs(AQUI / "renders" / "stills_v5", exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING="utf-8", NODE_PATH=NODE_PATH, CHROMIUM_PATH=r"C:/Program Files/Google/Chrome/Application/chrome.exe")
pedir = set(sys.argv[1:])
for nome, lote, aid, frase, dt, tem3d in STILLS:
    if pedir and nome not in pedir:
        continue
    T = instante(lote, aid, frase, dt)
    f = int(round(T * 15))
    if tem3d:
        so = ",".join(str(q) for q in range(max(0, f - 2), f + 50))
        subprocess.run(["node", "r3d.js", "--lote", lote, "--w", "1920", "--h", "1080", "--so", so], cwd=AQUI / "threejs", env=env,
                       stdout=subprocess.DEVNULL, check=True)
    md = AQUI / f"media_still_{lote}"
    subprocess.run([PY, "-m", "manim", "-r", "1920,1080", "--fps", "15", "--progress_bar", "none", "-s", "cena.py", lote], cwd=AQUI,
                   env=dict(env, MEDIA_DIR=str(md), STILL=str(T)), stdout=open(AQUI / f"log_still_{lote}.txt", "w"), stderr=subprocess.STDOUT)
    png = max(md.rglob(f"{lote}*.png"), key=lambda p: p.stat().st_mtime)
    shutil.copy(png, AQUI / "renders" / "stills_v5" / f"{nome}.png")
    print(f"{nome}.png @ {T:.2f} s (lote {lote})", flush=True)
