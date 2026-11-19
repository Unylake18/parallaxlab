#!/bin/bash
# yt_0030: passada de auditoria (sem gravar quadros) com o QA R5 em cada gatilho. uso: ./auditar.sh LOTE ... → log_sob_<LOTE>.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in "$@"; do
  (SO_AUDITORIA=1 QA_SOBREPOS=1 MEDIA_DIR="$PWD/media_aud_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching cena.py $C > "log_sob_$C.txt" 2>&1; rm -rf "media_aud_$C") &
done
wait
for C in "$@"; do echo "== $C $(grep -c '\[sobrepos\]' log_sob_$C.txt) ocorrências; $(grep -c 'sobrepos-chk' log_sob_$C.txt) checagens"; done
