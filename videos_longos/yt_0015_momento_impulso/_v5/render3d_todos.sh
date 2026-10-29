#!/bin/bash
# renderiza os três trechos 3D do v2 (960×540/15) em sequência → threejs/frames3d_<trecho>_960x540/
cd "$(dirname "$0")/threejs"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
for tr in "$@"; do rm -rf frames3d_${tr}_960x540; node render3d.js --trecho $tr > ../log_3d_$tr.txt 2>&1; tail -1 ../log_3d_$tr.txt; done
