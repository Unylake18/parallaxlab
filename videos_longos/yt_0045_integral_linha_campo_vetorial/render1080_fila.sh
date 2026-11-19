#!/bin/bash
# yt_0045 final §8: fila 1080p um lote por vez, com até 4 tentativas quando a máquina fica sem memória (outra unidade pode ocupar a RAM).
cd "$(dirname "$0")"
for C in "$@"; do
  for k in 1 2 3 4; do
    T0=$(date +%s)
    timeout 14400 ./render1080.sh $C > /dev/null 2>&1
    if grep -q "Traceback" log1080_$C.txt || ! grep -q "\[tempo\] total" log1080_$C.txt; then
      echo "$C tentativa $k falhou ($(grep -o 'MemoryError' log1080_$C.txt | head -1))"; sleep 180
    else
      echo "$C $(( $(date +%s) - T0 ))s $(grep -c '^\[R5\]' log1080_$C.txt) R5 $(grep -o 'deriva\] [A-Z0-9]* [-+0-9.]*s' log1080_$C.txt)"; break
    fi
  done
done
