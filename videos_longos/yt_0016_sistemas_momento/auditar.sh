#!/bin/bash
# auditoria de sobreposição de textos (dry run, sem render): ./auditar.sh Classe → audit_<Classe>.txt
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
AUDITORIA=1 PYTHONIOENCODING=utf-8 MEDIA_DIR="$PWD/media_aud_$1" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $1 2>&1 | grep "\[audit\]" | sort -u > "audit_$1.txt"
echo "$1: $(wc -l < audit_$1.txt) linhas"
