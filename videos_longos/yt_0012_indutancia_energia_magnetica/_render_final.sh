#!/bin/sh
# yt_0012 — passe a seco + ritmo + render final 1080p30 (CRF 14 automático pelo template) em 4 grupos, UM processo por vez.
set -e
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0012_indutancia_energia_magnetica
uv run --no-sync python -m py_compile $D/cena.py
rm -f $D/sync_log.jsonl
SEG=nenhuma SYNC_LOG=$D/sync_log.jsonl uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir $D/media_seco -o seco $D/cena.py IndutanciaYT012 > $D/seco.log 2>&1
(cd $D && PYTHONIOENCODING=utf-8 uv run --no-sync python ritmo.py | head -3)
n=0
for g in c01,c02,c03,c04,c05 c06,c07,c08,c09 c10,c11,c12,c13,c14 c15,c16,c17,c18,c19,c20,c20b; do
  n=$((n+1))
  echo "grupo $n: $g  $(date +%H:%M)"
  SEG=$g SYNC=$D/ritmo.json uv run --no-sync python -m manim -r 1920,1080 --fps 30 --media_dir $D/media_final -o grupo$n $D/cena.py IndutanciaYT012 > $D/render_g$n.log 2>&1
  tail -1 $D/render_g$n.log
done
echo "fim $(date +%H:%M)"
