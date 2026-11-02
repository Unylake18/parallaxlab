#!/bin/bash
# yt_0018 v7: passe de MEDIÇÃO (a seco, sem desenhar): mede o tempo nominal de animação (A) e de espera (W) de cada trecho entre marcas (início de âncora,
# gatilho, fração) → medicao_<Classe>.json. O render final (SYNC=final) usa essa medição em plano() para esticar cada trecho até a próxima palavra.
# uso: ./medir.sh Classe
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
TRES="PH PX2 PX3 PEP"
if [[ " $TRES " == *" $C "* ]]; then P=1; else P=0; fi
SYNC=medir PEDIDOS3D=$P SO_AUDITORIA=1 MEDIA_DIR="$PWD/media_med_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_med_$C.txt" 2>&1
grep -E "\[tempo\] total|Error|Traceback" "log_med_$C.txt" | tail -3
