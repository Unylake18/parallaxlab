#!/bin/bash
# yt_0019 v9: passe de MEDIÇÃO (a seco, sem desenhar): mede o tempo nominal de animação (A) e de espera (W) de cada trecho entre marcas (início de âncora,
# gatilho, fração) → medicao_<Classe>.json. O render final (SYNC=final) usa essa medição em plano() para esticar/encolher cada trecho até a próxima palavra.
# uso: ./medir.sh Classe
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
SYNC=medir SO_AUDITORIA=1 MEDIA_DIR="$PWD/media_med_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_med_$C.txt" 2>&1
echo "$C $(grep -E '\[tempo\] total|Error|Traceback' "log_med_$C.txt" | tail -2 | tr '\n' ' ')"
