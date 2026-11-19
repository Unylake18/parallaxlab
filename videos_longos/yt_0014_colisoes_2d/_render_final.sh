#!/bin/sh
# yt_0014 — render final 1080p30 (CRF 14 automático pelo template) em 5 grupos de seções, UM processo por vez.
# Pré-requisito: ritmo.json (GRAVAR=1 SECOES=nenhuma ... ; python ritmo.py). Depois: montar_sync.py, montar_final.py.
set -e
cd /c/Users/Pichau/PycharmProjects/manim-fisica
export PYTHONIOENCODING=utf-8
D=videos_longos/yt_0014_colisoes_2d
uv run --no-sync python -m py_compile $D/cena.py
rm -rf $D/media_final
n=0
for g in hook,abertura,c01,c02,c03 c04,c05,c06 c07,c08 c09,c10,c11 c12,c13,c14,cta; do
  n=$((n+1))
  echo "grupo $n: $g  $(date +%H:%M)"
  SECOES=$g uv run --no-sync python -m manim -r 1920,1080 --fps 30 --media_dir $D/media_final -o grupo$n $D/cena.py Colisoes2DYT014 > $D/render_g$n.log 2>&1
  grep -a "\[sync\]" $D/render_g$n.log | tr '\r' '\n' | tail -1
done
echo "fim $(date +%H:%M)"
