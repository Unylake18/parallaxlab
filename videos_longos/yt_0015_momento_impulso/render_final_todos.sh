#!/bin/bash
# render final 1920×1080/30 fps: 3D (hook, e4, cavalo) + projeções → camadas PH/PG4/PF2 → 10 lotes (4 em paralelo) → composições → vídeo final
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" FPS3D=30
date
"$PY" gerar_timelines.py | tail -5
(
  cd threejs
  for tr in hook e4 cavalo; do rm -rf frames3d_${tr}_1920x1080; node render3d.js --trecho $tr --w 1920 --h 1080 --fps 30 | tail -1; done
  node qa/muro_proj.js --trecho hook | tail -1
  node qa/muro_proj.js --trecho e4 | tail -1
  node qa/proj_quadros.js --trecho hook | tail -1
  node qa/proj_quadros.js --trecho cavalo | tail -1
  cd ..
  for c in PH PG4 PF2; do AUDITORIA=1 ./render_final.sh $c -t > /dev/null; echo "camada $c: $(grep -c Traceback logf_$c.txt) erros; $(grep -h 'camada\]' logf_$c.txt)"; done
) > log_final_3d.txt 2>&1 &
lote(){ for c in "$@"; do ( AUDITORIA=1 ./render_final.sh $c > /dev/null ) & done; wait; }
lote PE PG PD PT1
lote PT3 PF PC PB
lote PA PS
wait
cat log_final_3d.txt
for c in PA PT1 PB PT3 PC PD PE PF PG PS; do echo "== $c: $(grep -c Traceback logf_$c.txt) erros; $(grep -h '\[sync\]' logf_$c.txt) $(grep -c '^\[audit\]\|^\[orfao\]' logf_$c.txt) sobrep/órfãos"; done
grep -h "^\[audit\]\|^\[orfao\]" logf_P*.txt
"$PY" compor.py --trecho hook --classe PH --res 1920x1080 --fps 30 | tail -1
"$PY" compor.py --trecho e4 --classe PG4 --res 1920x1080 --fps 30 | tail -1
"$PY" compor.py --trecho cavalo --classe PF2 --res 1920x1080 --fps 30 | tail -1
"$PY" montar_sync.py --final
date
