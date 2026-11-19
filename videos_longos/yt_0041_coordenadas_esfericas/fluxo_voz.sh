#!/bin/bash
# yt_0041 final §6/§7: para cada lote, PRESSA=grava (passada seca) → render 540p/15 fps seguindo a voz (3D: pedidos → r3d → render). uso: ./fluxo_voz.sh LOTE...
cd "$(dirname "$0")"
export RODADA=v5
for C in "$@"; do
  ./pressa.sh $C
  if [ "$C" = "PA" ]; then ./render.sh PA > /dev/null 2>&1; else ./render3d.sh $C > /dev/null 2>&1; fi
  if grep -q "Traceback" "log_$C.txt"; then echo "FALHA $C"; else echo "ok $C $(tail -n 1 log_$C.txt) $(grep -c '\[estouro\]' log_$C.txt) estouros"; fi
done
echo FIM_FLUXO
