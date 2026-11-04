#!/bin/bash
# yt_0022: renderiza os lotes pedidos em paralelo (2D: render.sh; com 3D: render3d.sh). uso: ./render_todos.sh PT1 PT2 ...
cd "$(dirname "$0")"
TRES="PH PT1 PT2 PT4 PS"
for C in "$@"; do
  if [[ " $TRES " == *" $C "* ]]; then ./render3d.sh $C > /dev/null 2>&1 & else ./render.sh $C > /dev/null 2>&1 & fi
done
wait
for C in "$@"; do echo "== $C"; grep -E "\[tempo\] total|Error|Exception" log_$C.txt | tail -2; done
