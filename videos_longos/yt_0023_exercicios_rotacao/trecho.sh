#!/bin/bash
# Render por trecho (v7→v8). uso: ./trecho.sh LOTE ANC_INI [ANC_FIM] [--3d]
#   Re-renderiza só as âncoras ANC_INI..ANC_FIM (inclusive; só ANC_INI se FIM omitido) do lote e emenda o trecho no preview
#   media_<LOTE>/videos/cena/540p15/<LOTE>.mp4 (backup em <LOTE>.antes_trecho.mp4). Os planos anteriores rodam sem desenhar (-n).
#   --3d: regenera também os PNGs do 3D dos quadros do trecho (use se mudou algo do 3D); sem ele, reaproveita threejs/q3d.
#   Auditoria só do trecho: ./trecho.sh imprime o flash do intervalo (flash23.py --de/--ate se existir); auditoria completa só no fechamento.
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
export NODE_PATH="$(cd ../yt_0022_torque/threejs && pwd)/node_modules"
L=$1; A=$2; B=${3:-$2}; [ "$B" = "--3d" ] && B=$A
T3D=0; for x in "$@"; do [ "$x" = "--3d" ] && T3D=1; done
a0=$(date +%s)
# 1) passagem seca: índices (âncora → quadro, play) e pedidos do 3D
[ -f "log_idx_$L.txt" -a "$REIDX" != 1 ] || SO_AUDITORIA=1 PEDIDOS3D=1 MEDIA_DIR="$PWD/media_${L}_idx" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $L > "log_idx_$L.txt" 2>&1   # REIDX=1 refaz o mapa (só se mudou a duração/número de plays)
read -r q0 p0 < <(grep "^\[idx\] $A " "log_idx_$L.txt" | head -1 | awk '{print $3, $4}')
if grep -q "^\[idx\] $B " "log_idx_$L.txt" && [ "$B" != "$A" -o 1 = 1 ]; then
  # fim do trecho = início da âncora seguinte à B
  read -r q1 p1 < <(awk -v b="$B" '$1=="[idx]"{ if(f){print $3, $4; exit} if($2==b) f=1 }' "log_idx_$L.txt")
fi
[ -z "$q0" -o -z "$q1" ] && { echo "âncora não achada em log_idx_$L.txt"; exit 1; }
echo "trecho $A..$B: quadros $q0..$q1 (plays $p0..$((p1-1)))"
a1=$(date +%s)
# 2) 3D só dos quadros do trecho (opcional)
if [ $T3D = 1 ]; then
  so=$(seq -s, $q0 $((q1-1)))
  (cd threejs && node r3d.js --lote $L --so "$so") > "log_3d_trecho_$L.txt" 2>&1; tail -1 "log_3d_trecho_$L.txt"
fi
# 3) render só dos plays do trecho
rm -rf "media_${L}_t"
AUDITORIA=0 MEDIA_DIR="$PWD/media_${L}_t" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching -n $p0,$((p1-1)) cena.py $L > "log_t_$L.txt" 2>&1
a2=$(date +%s)
# 4) emenda
"$PY" emenda.py $L $q0 $q1 "media_${L}_t/videos/cena/540p15/$L.mp4"
a3=$(date +%s)
echo "tempo: seco=$((a1-a0))s render=$((a2-a1))s emenda=$((a3-a2))s total=$((a3-a0))s"
