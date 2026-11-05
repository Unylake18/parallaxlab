#!/bin/bash
# yt_0020 (copiado do yt_0019): passada só de auditoria (AUDITORIA=1, sem desenhar os quadros; os PNGs do 3D já precisam existir). uso: ./auditar.sh Classe [pasta]
#   → log_aud_<Classe>.txt (linhas [audit] e [dens]). Com `pasta`, roda o código daquela pasta (ex.: _teste_v2, o v2 com a auditoria nova).
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
D=${2:-.}
OUT="$PWD/log_aud_${C}${2:+_$(basename $D)}.txt"
(cd "$D" && SO_AUDITORIA=1 AUDITORIA=1 MEDIA_DIR="$PWD/media_aud_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching --dry_run cena.py $C > "$OUT" 2>&1)
grep -E "\[tempo\] total|Error" "$OUT" | tail -2
