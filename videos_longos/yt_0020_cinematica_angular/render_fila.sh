#!/bin/bash
# yt_0020: render_v3 dos lotes pedidos, dois de cada vez (uso: ./render_fila.sh PT1 PT2 ...)
cd "$(dirname "$0")"
for C in "$@"; do
  ./render_v3.sh $C > log_v3run_$C.txt 2>&1 &
  while [ $(jobs -r | wc -l) -ge 2 ]; do wait -n; done
done
wait
for C in "$@"; do echo "== $C $(grep -E '\[tempo\] total' log_$C.txt | tail -1)"; done
