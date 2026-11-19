#!/bin/bash
# yt_0036: passada seca (--dry_run) de um lote: acha erros, gatilhos sem frase, estouros, R5 e flash sem gravar vídeo. Log: log_seco_<C>.txt
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
MEDIA_DIR="$PWD/media_seco_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching "$@" cena.py $C > "log_seco_$C.txt" 2>&1
grep -E "Error|Traceback|gatilho-sem|estouro|\[R5|flash\]|deriva|tempo\] total" "log_seco_$C.txt" | head -40
