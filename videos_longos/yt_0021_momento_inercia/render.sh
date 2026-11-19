#!/bin/bash
# yt_0021 (copiado do yt_0019). uso: ./render.sh Classe [ -- extra ]  → media_<Classe>/videos/cena/540p15/<Classe>.mp4 (preview 960×540 / 15 fps); a auditoria de
# v3: o render não audita (AUDITORIA=0); a auditoria roda à parte em ./auditar.sh (log_aud_<Classe>.txt), em paralelo. Sem cache do Manim: um trecho em cache
# não roda as camadas quadro a quadro (perde o registro do QA) e não enxerga mudanças nos PNGs do 3D.
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
AUDITORIA=${AUDITORIA:-0} MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching "$@" cena.py $C > "log_$C.txt" 2>&1
tail -3 "log_$C.txt"
