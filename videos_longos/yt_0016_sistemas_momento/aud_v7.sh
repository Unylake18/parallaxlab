#!/bin/bash
# v7: uma passagem seca com AUDITORIA=1 CONTRASTE=1 por lote → audit_<L>.txt (sobreposições) e contr_<L>.txt (caixas/cores dos textos)
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
for C in "$@"; do
  AUDITORIA=1 CONTRASTE=1 PYTHONIOENCODING=utf-8 MEDIA_DIR="$PWD/media_aud_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_aud_$C.txt" 2>&1
  grep "\[audit\]" "log_aud_$C.txt" | sort -u > "audit_$C.txt"; grep "\[contraste\]" "log_aud_$C.txt" > "contr_$C.txt"
  echo "$C: audit $(wc -l < audit_$C.txt), contraste $(wc -l < contr_$C.txt), erros $(grep -c Traceback log_aud_$C.txt)"
done
