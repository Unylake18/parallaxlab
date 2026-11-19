#!/bin/bash
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
printf "%s\n" "$@" | xargs -P 4 -I{} bash -c '"'"$PY"'" corop24.py {} > log_cop_{}.txt 2>&1'
echo FIM > cop_v5.fim
