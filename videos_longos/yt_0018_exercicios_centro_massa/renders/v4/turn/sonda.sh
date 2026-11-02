#!/bin/bash
# turntable v3 do gafanhoto: 8 vistas (a cada 45°, pose parada) + 4 poses de perfil (0 agachado · 1 impulso · 2 voo · 3 pouso)
cd "$(dirname "$0")/../../../threejs"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
O=../renders/v4/turn
i=0
for az in -90 -45 0 45 90 135 180 -135; do
  node r3d.js --sonda lago --png $O/a$i.png --estado "{\"g\":{\"x\":0,\"z\":0,\"esc\":1.5,\"pose\":3},\"f\":{\"x\":-0.12,\"bal\":0},\"tw\":0,\"agua\":0,\"cam\":{\"modo\":\"obl\",\"az\":$az,\"el\":14,\"alvo\":[0.005,0,0.012],\"K\":62,\"xc\":0,\"yc\":-0.4,\"fov\":16}}" > /dev/null; i=$((i+1))
done
for p in 0 1 2 3; do
  node r3d.js --sonda lago --png $O/p$p.png --estado "{\"g\":{\"x\":0,\"z\":0.01,\"esc\":1.5,\"pose\":$p},\"f\":{\"x\":-0.12,\"bal\":0},\"tw\":0,\"agua\":0,\"cam\":{\"modo\":\"obl\",\"az\":-90,\"el\":4,\"alvo\":[0.0,0,0.015],\"K\":50,\"xc\":0,\"yc\":-0.3,\"fov\":16}}" > /dev/null
done
