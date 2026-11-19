#!/bin/bash
# yt_0037: passada seca de um lote (sem render de quadros; acha erros, gatilhos, R5 e flash rápido). uso: ./seco.sh LOTE
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
MEDIA_DIR="$PWD/media_seco_$C" timeout 1800 "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_seco_$C.txt" 2>&1
grep -E "Traceback|Error|error:|gatilho-sem|estouro|\[R5\]|\[flash\]|pecas\] AVISO|deriva|tempo\] total" "log_seco_$C.txt" | head -40
