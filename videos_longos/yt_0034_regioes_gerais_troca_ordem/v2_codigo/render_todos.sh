#!/bin/bash
# yt_0034: fila de render do preview (lotes 2D com render.sh, lotes 3D com render3d.sh), com timeout por lote. uso: ./render_todos.sh [LOTES...]
cd "$(dirname "$0")"
L=${@:-PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PB8 PS}
for C in $L; do
  T0=$(date +%s)
  case " PB3 PB4 " in *" $C "*) timeout 5400 ./render3d.sh $C > /dev/null 2>&1 ;; *) timeout 3600 ./render.sh $C > /dev/null 2>&1 ;; esac
  echo "$C $(( $(date +%s) - T0 ))s $(grep -c '\[R5\]' log_$C.txt) R5 $(grep -o 'flash-total\] [A-Z0-9]* [0-9]*' log_$C.txt | awk '{print $3}') flash $(grep -o 'deriva\] [A-Z0-9]* [-+0-9.]*s' log_$C.txt | awk '{print $3}') $(grep -l 'Traceback' log_$C.txt >/dev/null && echo ERRO)"
done
