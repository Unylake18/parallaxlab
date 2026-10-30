#!/bin/bash
# v7: QA de contraste — passagem seca com AUDITORIA=1 CONTRASTE=1: caixas e cores dos textos a cada 0,5 s → contr_<Classe>.txt
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
for C in "$@"; do
  AUDITORIA=1 CONTRASTE=1 PYTHONIOENCODING=utf-8 MEDIA_DIR="$PWD/media_aud_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C 2>&1 | grep "\[contraste\]" > "contr_$C.txt"
  echo "$C: $(wc -l < contr_$C.txt) linhas"
done
