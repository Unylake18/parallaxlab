#!/bin/bash
# yt_0034 v2: passada de auditoria (sem gravar vídeo) com o R5 contínuo a cada 0,2 s + folga 12 px + painel × palco. uso: ./auditar.sh [LOTES]
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in ${@:-PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PB8 PS}; do
  AUDIT_V2=1 SO_AUDITORIA=1 MEDIA_DIR="$PWD/media_audit_$C" timeout 1800 "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching cena.py $C > "log_audit_$C.txt" 2>&1
  echo "$C R5=$(grep -c '^\[R5' log_audit_$C.txt) F=$(grep -c '^\[R5F' log_audit_$C.txt) P=$(grep -c '^\[R5P' log_audit_$C.txt) $(grep -l Traceback log_audit_$C.txt >/dev/null && echo ERRO)"
done
