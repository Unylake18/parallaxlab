#!/bin/bash
cd "$(dirname "$0")"
PY=../../.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8 CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
for L in PH PT1 PT2 PT3 PT4; do $PY corop.py $L > log_cop_$L.txt 2>&1 & done; wait
for L in PT5 PE1 PE2 PE3 PS; do $PY corop.py $L > log_cop_$L.txt 2>&1 & done; wait
$PY prancha_humana.py v7 > log_ph7.txt 2>&1
$PY conferencia20.py v7 > log_conf_v7.txt 2>&1
$PY qa20.py v7 > log_qa7.txt 2>&1
echo QAFIM > log_qa_fim7.txt
