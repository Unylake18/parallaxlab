#!/bin/bash
# render FINAL (2ª passada, depois da correção do realce em segundos no kit.wait): como final_v7.sh, mas reaproveita os quadros 3D
# do render anterior com o mesmo estado (r3d.js --reusa). uso: ./final2_v7.sh L1 L2 ...
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export NODE_PATH="$(cd ../yt_0015_momento_impulso/threejs/node_modules && pwd -W 2>/dev/null || pwd)"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
for C in "$@"; do
  Q="threejs/q3d/${C}_1920x1080"
  if [ -d "$Q" ] && [ ! -d "${Q}_ant" ]; then mv "$Q" "${Q}_ant"; cp "threejs/pedidos3d/$C.json" "${Q}_ant/pedidos.json"; fi
  PEDIDOS3D=1 MEDIA_DIR="$PWD/media_pedf_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --dry_run cena.py $C > "log_pedf_$C.txt" 2>&1
  echo "$C seco: $(grep -c Traceback log_pedf_$C.txt) erros; $(grep '\[tempo\] total\|\[3d\]' log_pedf_$C.txt | tr '\n' ' ')"
  if grep -q '\[3d\]' "log_pedf_$C.txt"; then
    rm -rf "$Q"
    R=""; [ -d "${Q}_ant" ] && R="--reusa $(cd "${Q}_ant" && pwd -W 2>/dev/null || pwd)"
    (cd threejs && node r3d.js --lote $C --w 1920 --h 1080 $R) > "log_3df_$C.txt" 2>&1
    echo "$C 3d: $(tail -n 1 log_3df_$C.txt)"
  fi
  MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none cena.py $C > "logf_$C.txt" 2>&1
  echo "$C: $(grep 'tempo\] total' logf_$C.txt) $(grep -c Traceback logf_$C.txt) erros $(grep -h '\[atraso\]' logf_$C.txt | tr '\n' ' ')"
  if ! grep -q Traceback "logf_$C.txt" && grep -q 'tempo\] total' "logf_$C.txt"; then rm -rf "${Q}_ant"; fi   # libera o disco
done
