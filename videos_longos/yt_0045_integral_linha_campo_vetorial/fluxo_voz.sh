#!/bin/bash
# yt_0045 final §6/§7: para cada lote, PRESSA=grava (passada seca) → render 540p/15 fps seguindo a voz. uso: ./fluxo_voz.sh LOTE...
cd "$(dirname "$0")"
export RODADA=final
export PISO_PRESSA=1.0
for C in "$@"; do
  ./pressa.sh $C
  ./render.sh $C > /dev/null 2>&1
  if grep -q "Traceback" "log_$C.txt"; then echo "FALHA $C"; else echo "ok $C $(tail -n 1 log_$C.txt) $(grep -c '\[estouro\]' log_$C.txt) estouros"; fi
done
echo FIM_FLUXO
