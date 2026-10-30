#!/bin/bash
# v7: passagem seca + 3D + render de cada lote, em sequência: ./lote_v7.sh L1 L2 ...
cd "$(dirname "$0")"
for C in "$@"; do ./seco_v3.sh $C; ./fila_v3.sh $C; done
