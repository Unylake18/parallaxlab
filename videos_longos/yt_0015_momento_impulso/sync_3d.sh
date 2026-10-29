#!/bin/bash
# sincronia: timelines 3D com as durações reais (ancoras.json da voz) → render hook/e4/cavalo → projeções de rótulos
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
"$PY" gerar_timelines.py
./render3d_todos.sh hook e4 cavalo
cd threejs
node qa/muro_proj.js --trecho hook | tail -1
node qa/muro_proj.js --trecho e4 | tail -1
node qa/proj_quadros.js --trecho hook | tail -1
node qa/proj_quadros.js --trecho cavalo | tail -1
