"""Stills 1920×1080 das itens do v6 (handoff v6 §5: tabela 1.2 e N1–N8) → renders/stills_v6/.
Instante = quando a voz diz a frase (ancoras.json) + atraso, no relógio do lote (o lote começa na sua primeira âncora).
Lotes com fundo 3D: o r3d.js renderiza em 1920×1080 só os quadros perto do instante (a partir dos pedidos da passagem seca).
uso: python stills_v6.py [nome ...]"""
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
    ("12_T9-3_disparo_congelado", "P9", "T9-3", "a dois metros por segundo", 0.6, False),
    ("12_T10-1_barras_momento", "P10", "T10-1", "Em tamanho", 0.2, False),
    ("12_E6-1_bola_parada_no_ar", "Q6", "E6-1", "O sistema é você mais a bola", 1.2, True),
    ("12_E6-3_rebate", "Q6", "E6-3", "Agora ela perde", 0.3, True),
    ("12_E7-2_setas_iguais", "Q7", "E7-2", "A velocidade de recuo", 0.0, True),
    ("12_E8-1_rifle_recua", "Q8", "E8-1", "em relação ao chão", 0.8, False),
    ("12_E7-3_seta_riscada", "Q7", "E7-3", "Então quem segurou ele", 0.6, True),
    ("12_E9-5_previsao_de_newton", "Q9", "E9-5", "ao entrar na água", 0.6, False),
    ("12_EN2_granada", "PS", "EN2", "na mesma parábola", 0.2, False),
    ("12_S1_T_e_menos_T", "PS", "S1", "A corda puxa, sim", 1.0, True),
    ("N1_T8-8_dica", "P8", "T8-8", "Por isso andar no gelo", 0.8, True),
    ("N2_E7-5_chips", "Q7", "E7-5", "E a energia", 0.5, True),
    ("N3_N4_E9-5_refracao", "Q9", "E9-5", "a luz se aproxima da normal", 1.2, False),
    ("N5_C-2_fotons_na_vela", "PC", "C-2", "Uma vela solar refletora", 0.5, True),
    ("N6_E7-4_decomposicao", "Q7", "E7-4", "Só a parte horizontal", 0.2, True),
    ("N7_E6-4_eletica_e_dica", "Q6", "E6-4", "Ela só se conserva", 1.6, True),
    ("N8_T9-2_mg_e_cota", "P9", "T9-2", "Ninguém percebe", 0.5, False),
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


os.makedirs(AQUI / "renders" / "stills_v6", exist_ok=True)
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
    shutil.copy(png, AQUI / "renders" / "stills_v6" / f"{nome}.png")
    print(f"{nome}.png @ {T:.2f} s (lote {lote})", flush=True)
