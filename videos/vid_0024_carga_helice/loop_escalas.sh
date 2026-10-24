#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica/videos/vid_0024_carga_helice
: > loop.log
for i in 1 2 3 4; do
  rm -f chegada.json
  bash iterar.sh
  python calcular_escalas.py chegada >> loop.log 2>&1
  if tail -3 loop.log | grep -q "atrasados: \[\]"; then echo "convergiu na passada $i" >> loop.log; break; fi
done
echo done >> loop.log
