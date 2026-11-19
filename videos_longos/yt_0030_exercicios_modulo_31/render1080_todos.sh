#!/bin/bash
# yt_0030 final §7.1: os 12 lotes em 1080p30 sem perdas (CRF=0), 6 por vez, com limite de 3 h por lote (trava de LaTeX não fica silenciosa).
cd "$(dirname "$0")"
: > log1080_custo.txt
um() { local t0=$(date +%s); timeout 10800 ./render1080.sh $1 > /dev/null 2>&1; local rc=$?; echo "$1 $(( $(date +%s) - t0 )) s saída=$rc" >> log1080_custo.txt; }
for C in PD3 PD4 PD5 PD1 PA3 PD3B; do um $C & done; wait
for C in PA1 PA2 PA4 PH PS PD2; do um $C & done; wait
for C in PH PD1 PD2 PD3 PD3B PD4 PD5 PA1 PA2 PA4 PA3 PS; do echo "== $C $(grep -E '\[tempo\] total' log1080_$C.txt | tail -1) $(grep -c Traceback log1080_$C.txt) $(ls -la media1080_$C/videos/cena/1080p30/$C.mp4 2>/dev/null | awk '{print $5}')"; done
