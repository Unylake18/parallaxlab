#!/bin/bash
# sonda de um estado: ./sonda.sh '<json do estado>' saida.png [W H]
cd "$(dirname "$0")"
export NODE_PATH="$(cd ../../yt_0022_torque/threejs && pwd)/node_modules"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
node r3d.js --sonda ${5:-mesa_furo} --estado "$1" --png "$2" --w ${3:-960} --h ${4:-540}
