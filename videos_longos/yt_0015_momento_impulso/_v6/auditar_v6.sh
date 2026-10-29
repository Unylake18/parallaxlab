#!/bin/bash
# QA v6 sem render (--dry_run): folga mínima entre textos por âncora, legibilidade, órfãos e escrita → audit6_<Classe>.txt
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
for c in "$@"; do
  ( AUDITORIA=1 PYTHONIOENCODING=utf-8 MEDIA_DIR="$PWD/media_aud6_$c" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $c 2>&1 \
      | grep -E "^\[(folga|legib|orfao|escrita|audit)" | sort -u > audit6_$c.txt ) &
done
wait
for c in "$@"; do echo "== $c: $(wc -l < audit6_$c.txt) linhas"; done
