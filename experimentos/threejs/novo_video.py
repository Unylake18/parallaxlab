"""Cria uma unidade nova de vídeo Three.js + Manim a partir do modelo.

Uso (na raiz do repositório):
  uv run python experimentos/threejs/novo_video.py vid_0031_nome_curto

Copia experimentos/threejs/modelo/ para videos/<nome>/ e põe o Three.js r128 (vendor) dentro de cena3d/, para a
unidade funcionar sozinha. Recusa se a pasta já existir (nunca sobrescreve um vídeo).
"""
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]

if len(sys.argv) != 2 or not sys.argv[1].startswith(("vid_", "yt_")):
    sys.exit("uso: novo_video.py vid_NNNN_nome   (ou yt_NNNN_nome para longo)")
nome = sys.argv[1]
base = ROOT / ("videos_longos" if nome.startswith("yt_") else "videos")
dest = base / nome
if dest.exists():
    sys.exit(f"já existe: {dest}")
shutil.copytree(AQUI / "modelo", dest, ignore=shutil.ignore_patterns("node_modules", "frames3d_*", "media_preview", "renders"))
for arq in (AQUI / "vendor" / "three-r128").iterdir():
    shutil.copy2(arq, dest / "cena3d" / arq.name)
print(f"criado: {dest}")
if nome.startswith("yt_"):
    print("AVISO: o modelo é vertical 9×16. Para longo, troque o quadro (16×9) no cena.py, no render3d.js e no QA.")
print("próximos passos: cd na pasta, npm install, node render3d.js --quadros 0,60,100 (ver README do experimentos/threejs)")
