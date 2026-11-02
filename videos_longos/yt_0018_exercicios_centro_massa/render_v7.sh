#!/bin/bash
# yt_0018 v7: renderiza os lotes (3D: pedidos → Three.js → Manim; 2D: Manim) com a medição já feita (medicao_<Classe>.json) e a voz contínua.
# uso: ./render_v7.sh PH PX3 ...   (até 4 lotes ao mesmo tempo)
cd "$(dirname "$0")"
printf "%s\n" "$@" | xargs -P 4 -I{} ./render_v3.sh {}
