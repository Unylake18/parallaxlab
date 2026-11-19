#!/bin/bash
# yt_0030 v4 §7.1: os 12 lotes em 1080p30 sem perdas (CRF=0), no máximo 4 por vez, cada um só começa com ≥ 8 GB de RAM livre (a máquina
# é dividida com outras unidades) e com limite de 3 h. O sucesso é conferido pelo log ([tempo] total) e pelo MP4, não pelo código de saída.
cd "$(dirname "$0")"
: > log1080_custo.txt
livre() { powershell -c "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" 2>/dev/null; }
um() {
  local C=$1 t0 ok
  for i in $(seq 1 180); do [ "$(livre)" -ge 8000 ] && break; sleep 60; done
  t0=$(date +%s)
  timeout 10800 ./render1080.sh $C > /dev/null 2>&1
  ok=$(grep -c "\[tempo\] total" log1080_$C.txt)
  [ -s media1080_$C/videos/cena/1080p30/$C.mp4 ] || ok=0
  echo "$C $(( $(date +%s) - t0 )) s ok=$ok" >> log1080_custo.txt
}
export -f um livre
printf "%s\n" PD3 PD4 PD5 PA3 PD1 PD3B PA1 PA2 PA4 PH PS PD2 | xargs -P 4 -I{} bash -c 'um {}; sleep 0'
for C in PH PD1 PD2 PD3 PD3B PD4 PD5 PA1 PA2 PA4 PA3 PS; do echo "== $C $(grep -E '\[tempo\] total' log1080_$C.txt) tb=$(grep -c Traceback log1080_$C.txt) sem=$(grep -c gatilho-sem-frase log1080_$C.txt)"; done
