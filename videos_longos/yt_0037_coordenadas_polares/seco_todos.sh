#!/bin/bash
# yt_0037: passada seca de todos os lotes (um por vez). uso: ./seco_todos.sh [LOTES...]
cd "$(dirname "$0")"
L=${@:-PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PS}
for C in $L; do
  T0=$(date +%s)
  ./seco.sh $C > /dev/null 2>&1
  echo "$C $(( $(date +%s) - T0 ))s | erro: $(grep -c 'Traceback' log_seco_$C.txt) | sem-frase: $(grep -c 'gatilho-sem-frase' log_seco_$C.txt) | estouro: $(grep -c '\[estouro\]' log_seco_$C.txt) | R5: $(grep -c '^\[R5[A-Z0-9]*\]' log_seco_$C.txt)"
done
