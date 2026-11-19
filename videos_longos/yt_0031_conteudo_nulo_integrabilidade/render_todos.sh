#!/bin/bash
# yt_0031: renderiza os lotes (3 em paralelo; os lotes com 3D passam pelo render3d.sh). uso: ./render_todos.sh [LOTE ...] (sem argumentos: todos)
cd "$(dirname "$0")"
L=${@:-PB1 PB7 PB2 PB6 PB4 PB3 PB5 PS PH PB8 PB9 PA}
um() { case " PB1 PB2 PB5 PB6 PS " in *" $1 "*) ./render3d.sh $1 > /dev/null 2>&1;; *) ./render.sh $1 > /dev/null 2>&1;; esac; }
export -f um
printf "%s\n" $L | xargs -P ${P:-3} -I{} bash -c 'um {}'
for C in $L; do echo "== $C $(grep -h '\[render\]' log_$C.txt | tail -1) $(cat tempo3d_$C.txt 2>/dev/null) $(grep -E '\[tempo\] total|Error|Exception' log_$C.txt | tail -1)"; done
