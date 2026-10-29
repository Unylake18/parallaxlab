#!/bin/bash
# uso: ./render.sh Classe [ -- extra ]  → media_<Classe>/videos/cena/540p15/<Classe>.mp4 (preview 960×540 / 15 fps); a auditoria de
# sobreposição e de PALCO vazio (AUDITORIA=1) sai no log_<Classe>.txt como linhas [audit]. Sem cache do Manim: um trecho em cache
# não roda as camadas quadro a quadro (perde o registro do QA) e não enxerga mudanças nos PNGs do 3D.
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
AUDITORIA=1 MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching "$@" cena.py $C > "log_$C.txt" 2>&1
tail -3 "log_$C.txt"
